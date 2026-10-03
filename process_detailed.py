import glob, json, cv2, os, re
import numpy as np
from rapidocr_onnxruntime import RapidOCR
from multiprocessing import Pool

def process_file_detailed(fpath):
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
    
    sku_indices = [i for i, l in enumerate(lines) if 'SKU' in l['text'].upper() and re.search(r'\d{5,}', l['text'])]
    
    file_products = []
    os.makedirs('drink_images', exist_ok=True)
    
    for s_idx in sku_indices:
        sku_line = lines[s_idx]
        sku_m = re.search(r'SKU\s*[:：]?\s*(\d+)', sku_line['text'], re.IGNORECASE)
        upc_m = re.search(r'UPC\s*[:：]?\s*(\d+)', sku_line['text'], re.IGNORECASE)
        sku = sku_m.group(1) if sku_m else ''
        upc = upc_m.group(1) if upc_m else ''
        
        if not upc and s_idx + 1 < len(lines):
            next_l = lines[s_idx + 1]
            if next_l['ymin'] - sku_line['ymax'] < 50:
                next_upc_m = re.search(r'UPC\s*[:：]?\s*(\d+)', next_l['text'], re.IGNORECASE)
                if next_upc_m:
                    upc = next_upc_m.group(1)
        
        # S_idx index in sku_indices
        pos_in_skus = sku_indices.index(s_idx)
        prev_limit = lines[sku_indices[pos_in_skus - 1]]['ymax'] if pos_in_skus > 0 else 520
        
        title_lines = []
        for l in lines:
            if l['xmin'] > 240 and prev_limit - 10 <= l['ymin'] < sku_line['ymin']:
                t = l['text']
                if 'Add to' not in t and 'Filter' not in t and 'Sort' not in t and 'Category' not in t and 'Product List' not in t and 'Order' not in t and 'Dashboard' not in t and 'Support' not in t and 'Profile' not in t:
                    if not re.match(r'^[0-9+\- ]+$', t):
                        title_lines.append(t)
        
        y_top = max(prev_limit + 10, sku_line['ymin'] - 270)
        y_bot = min(h - 150, sku_line['ymax'] + 210)
        
        crop_sub = img[int(y_top):int(y_bot), int(w*0.02):int(w*0.33)]
        crop_h, crop_w = 0, 0
        img_file = f'drink_images/sku_{sku}.png' if sku else ''
        
        if crop_sub.size > 0 and sku:
            gray = cv2.cvtColor(crop_sub, cv2.COLOR_BGR2GRAY)
            mask = gray < 248
            coords = np.argwhere(mask)
            if len(coords) > 150:
                cy0, cx0 = coords.min(axis=0)
                cy1, cx1 = coords.max(axis=0)
                cy0 = max(0, cy0 - 4)
                cy1 = min(crop_sub.shape[0], cy1 + 4)
                cx0 = max(0, cx0 - 4)
                cx1 = min(crop_sub.shape[1], cx1 + 4)
                cropped_bottle = crop_sub[cy0:cy1, cx0:cx1]
                crop_h, crop_w = cropped_bottle.shape[:2]
                
                # Check if we should save or overwrite if taller
                existing_file = f'drink_images/sku_{sku}.png'
                should_save = True
                if os.path.exists(existing_file):
                    ex_img = cv2.imread(existing_file)
                    if ex_img is not None and ex_img.shape[0] >= crop_h:
                        should_save = False
                if should_save and crop_h >= 100:
                    cv2.imwrite(existing_file, cropped_bottle)
        
        file_products.append({
            'file': os.path.basename(fpath),
            'sku': sku,
            'upc': upc,
            'sku_line': sku_line['text'],
            'title_lines': title_lines,
            'raw_name': ' '.join(title_lines),
            'img_path': f'drink_images/sku_{sku}.png' if sku else '',
            'crop_h': crop_h,
            'crop_w': crop_w
        })
        
    return file_products

if __name__ == '__main__':
    files = sorted(glob.glob('Screenshot_*.jpg'))
    print(f'Processing {len(files)} files in parallel...')
    with Pool(2) as pool:
        all_res = pool.map(process_file_detailed, files)
        
    flat = []
    for r in all_res:
        flat.extend(r)
        
    print(f'Total records: {len(flat)}')
    with open('all_detailed_products.json', 'w') as f:
        json.dump(flat, f, indent=2)
    print('Done!')
