import cv2
import numpy as np
import glob
import os
import json
import re
from rapidocr_onnxruntime import RapidOCR
from multiprocessing import Pool

def process_file_accurate_crops(fpath):
    ocr = RapidOCR()
    img = cv2.imread(fpath)
    if img is None:
        return []
    h, w = img.shape[:2]
    
    new_w = 1080
    scale = new_w / w
    new_h = int(h * scale)
    scaled = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    res, _ = ocr(scaled)
    if not res:
        return []
    
    lines = []
    for item in res:
        box, text, score = item[0], item[1], item[2]
        ymin = min(p[1] for p in box) / scale
        ymax = max(p[1] for p in box) / scale
        xmin = min(p[0] for p in box) / scale
        xmax = max(p[0] for p in box) / scale
        lines.append({'text': text.strip(), 'ymin': ymin, 'ymax': ymax, 'xmin': xmin, 'xmax': xmax, 'score': score})
    
    lines.sort(key=lambda x: x['ymin'])
    
    # Identify SKU lines
    sku_indices = [i for i, l in enumerate(lines) if 'SKU' in l['text'].upper() and re.search(r'\d{5,}', l['text'])]
    
    crops = []
    for pos, s_idx in enumerate(sku_indices):
        sku_line = lines[s_idx]
        sku_m = re.search(r'SKU\s*[:：]?\s*(\d+)', sku_line['text'], re.IGNORECASE)
        sku = sku_m.group(1) if sku_m else ''
        if not sku:
            continue
            
        # The drink image for this SKU is directly to the left of the title and SKU
        # Vertical range:
        # y_bottom: just below the SKU line / Add to cart button (sku_line['ymax'] + 80)
        # y_top: above the title for this SKU (sku_line['ymin'] - 240)
        # But not exceeding the previous SKU line
        prev_sku_ymax = lines[sku_indices[pos - 1]]['ymax'] if pos > 0 else 520
        y_top = max(prev_sku_ymax + 15, sku_line['ymin'] - 260)
        y_bottom = min(h - 120, sku_line['ymax'] + 70)
        
        # Horizontal range: bottle column (x: 4% to 28% of width)
        x_left = int(w * 0.04)
        x_right = int(w * 0.28)
        
        sub = img[int(y_top):int(y_bottom), x_left:x_right]
        if sub.size == 0:
            continue
            
        gray = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
        mask = gray < 246
        coords = np.argwhere(mask)
        if len(coords) < 100:
            continue
            
        cy0, cx0 = coords.min(axis=0)
        cy1, cx1 = coords.max(axis=0)
        
        # Add small padding
        pad = 4
        cy0 = max(0, cy0 - pad)
        cy1 = min(sub.shape[0], cy1 + pad)
        cx0 = max(0, cx0 - pad)
        cx1 = min(sub.shape[1], cx1 + pad)
        
        cropped_drink = sub[cy0:cy1, cx0:cx1]
        ch, cw = cropped_drink.shape[:2]
        
        if ch >= 80:
            crops.append({
                'sku': sku,
                'crop': cropped_drink,
                'height': ch,
                'width': cw,
                'file': os.path.basename(fpath)
            })
            
    return crops

if __name__ == '__main__':
    files = sorted(glob.glob('Screenshot_*.jpg'))
    print(f'Running accurate crops on {len(files)} files...')
    with Pool(2) as pool:
        all_res = pool.map(process_file_accurate_crops, files)
        
    flat = []
    for r in all_res:
        flat.extend(r)
        
    print(f'Total crops extracted: {len(flat)}')
    
    # Save highest crop per SKU
    by_sku = {}
    for item in flat:
        sku = item['sku']
        if sku not in by_sku or item['height'] > by_sku[sku]['height']:
            by_sku[sku] = item
            
    print(f'Unique SKUs with clean crops: {len(by_sku)}')
    
    os.makedirs('drink_images', exist_ok=True)
    for sku, item in by_sku.items():
        out_path = f"drink_images/sku_{sku}.png"
        cv2.imwrite(out_path, item['crop'])
        
    print("Successfully saved all clean accurate crops!")
