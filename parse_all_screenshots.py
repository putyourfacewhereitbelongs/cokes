import cv2
import os
import glob
import re
import json
import numpy as np
from rapidocr_onnxruntime import RapidOCR
from multiprocessing import Pool
from PIL import Image

def find_dividers(img):
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x_start = int(w * 0.1)
    x_end = int(w * 0.9)
    row_means = np.mean(gray[:, x_start:x_end], axis=1)
    row_stds = np.std(gray[:, x_start:x_end], axis=1)
    
    dividers = []
    # Search between top header (around y=550) and bottom nav bar (around y=h-200)
    for y in range(500, h - 150):
        if row_stds[y] < 6 and 210 < row_means[y] < 248:
            dividers.append(y)
            
    grouped = []
    if dividers:
        curr = [dividers[0]]
        for y in dividers[1:]:
            if y == curr[-1] + 1:
                curr.append(y)
            else:
                grouped.append(int(np.mean(curr)))
                curr = [y]
        if curr:
            grouped.append(int(np.mean(curr)))
    return grouped

def process_single_file(fpath):
    ocr = RapidOCR()
    img = cv2.imread(fpath)
    if img is None:
        return []
    h, w = img.shape[:2]
    
    new_w = 720
    scale = new_w / w
    new_h = int(h * scale)
    small = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    res, _ = ocr(small)
    if not res:
        return []
    
    boxes_text = []
    for item in res:
        box, text, score = item[0], item[1], item[2]
        orig_box = [[p[0]/scale, p[1]/scale] for p in box]
        ymin = min(p[1] for p in orig_box)
        ymax = max(p[1] for p in orig_box)
        xmin = min(p[0] for p in orig_box)
        xmax = max(p[0] for p in orig_box)
        boxes_text.append({
            'text': text.strip(),
            'ymin': ymin, 'ymax': ymax,
            'xmin': xmin, 'xmax': xmax,
            'score': score
        })
        
    dividers = find_dividers(img)
    
    # Identify SKU lines
    sku_items = []
    for i, b in enumerate(boxes_text):
        text = b['text']
        if re.search(r'SKU\s*[:：]?\s*\d+', text, re.IGNORECASE):
            sku_items.append((i, b))
            
    results = []
    os.makedirs('drink_images', exist_ok=True)
    
    for idx, (b_idx, sku_box) in enumerate(sku_items):
        sku_text = sku_box['text']
        sku_match = re.search(r'SKU\s*[:：]?\s*(\d+)', sku_text, re.IGNORECASE)
        upc_match = re.search(r'UPC\s*[:：]?\s*(\d+)', sku_text, re.IGNORECASE)
        sku = sku_match.group(1) if sku_match else ''
        upc = upc_match.group(1) if upc_match else ''
        
        # In case UPC is in the next line
        if not upc and b_idx + 1 < len(boxes_text):
            next_b = boxes_text[b_idx + 1]
            if next_b['ymin'] - sku_box['ymax'] < 50:
                next_upc = re.search(r'UPC\s*[:：]?\s*(\d+)', next_b['text'], re.IGNORECASE)
                if next_upc:
                    upc = next_upc.group(1)
        
        # Determine the vertical bounds for this item
        # Look for the preceding title lines above sku_box
        # Title lines have xmin > 280 and ymin < sku_box['ymin']
        # and ymin > previous sku_box ymax (or previous divider)
        prev_sku_ymax = sku_items[idx-1][1]['ymax'] if idx > 0 else 500
        
        # Find dividers around this item
        div_above = [d for d in dividers if d < sku_box['ymin'] and d >= prev_sku_ymax - 50]
        y_top = max(div_above) if div_above else max(520, sku_box['ymin'] - 280)
        
        # Next divider below
        div_below = [d for d in dividers if d > sku_box['ymax']]
        y_bottom = min(div_below) if div_below else min(h - 180, sku_box['ymax'] + 220)
        
        # Collect text lines belonging to this item
        item_texts = []
        for b in boxes_text:
            if b['xmin'] > 250 and y_top - 30 <= b['ymin'] and b['ymax'] <= y_bottom + 30:
                # Exclude 'Add to Cart', numbers in quantity, SKU line
                t = b['text']
                if 'Add to Cart' in t or 'Add toCart' in t:
                    continue
                if re.search(r'^\d+$', t):
                    continue
                if '+' in t or '-' in t and len(t) <= 3:
                    continue
                if 'SKU' in t.upper() or 'UPC' in t.upper():
                    continue
                item_texts.append(b)
                
        # Sort item_texts by ymin
        item_texts.sort(key=lambda x: x['ymin'])
        title_lines = [b['text'] for b in item_texts]
        raw_name = " ".join(title_lines)
        
        # Crop drink image from x: 20..320, y: y_top..y_bottom
        crop_y0 = max(0, int(y_top + 4))
        crop_y1 = min(h, int(y_bottom - 4))
        crop_x0 = max(0, int(w * 0.03))
        crop_x1 = min(w, int(w * 0.32))
        
        img_crop = img[crop_y0:crop_y1, crop_x0:crop_x1]
        img_filename = f"drink_{sku}.png" if sku else f"drink_item_{os.path.basename(fpath)}_{idx}.png"
        img_path = os.path.join('drink_images', img_filename)
        
        crop_height = 0
        crop_width = 0
        
        if img_crop.size > 0:
            gray_crop = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
            # Find non-white pixels
            mask = gray_crop < 248
            coords = np.argwhere(mask)
            if len(coords) > 100:
                cy0, cx0 = coords.min(axis=0)
                cy1, cx1 = coords.max(axis=0)
                pad_y = 6
                pad_x = 6
                cy0 = max(0, cy0 - pad_y)
                cy1 = min(img_crop.shape[0], cy1 + pad_y)
                cx0 = max(0, cx0 - pad_x)
                cx1 = min(img_crop.shape[1], cx1 + pad_x)
                bottle_crop = img_crop[cy0:cy1, cx0:cx1]
                crop_height = bottle_crop.shape[0]
                crop_width = bottle_crop.shape[1]
                
                # Check if it's a decent crop (at least 80px tall)
                if crop_height >= 80:
                    # Save with white border/transparent
                    # Let's write as PNG
                    cv2.imwrite(img_path, bottle_crop)
            
        results.append({
            'source_file': fpath,
            'sku': sku,
            'upc': upc,
            'raw_name': raw_name,
            'title_lines': title_lines,
            'image_path': img_path if crop_height >= 80 and os.path.exists(img_path) else '',
            'crop_height': crop_height,
            'crop_width': crop_width
        })
        
    return results

if __name__ == '__main__':
    files = sorted(glob.glob('Screenshot_*.jpg'))
    print(f'Starting extraction across {len(files)} files with 2 workers...')
    with Pool(2) as p:
        all_file_results = p.map(process_single_file, files)
        
    all_items = []
    for res in all_file_results:
        all_items.extend(res)
        
    print(f'Total items detected across all screenshots: {len(all_items)}')
    with open('extracted_raw_items.json', 'w') as f:
        json.dump(all_items, f, indent=2)
    print('Saved to extracted_raw_items.json')
