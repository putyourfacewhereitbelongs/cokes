import cv2
import numpy as np
import glob
import os
import json
import re
from rapidocr_onnxruntime import RapidOCR
from multiprocessing import Pool

def find_dividers(img):
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x_start = int(w * 0.1)
    x_end = int(w * 0.9)
    row_means = np.mean(gray[:, x_start:x_end], axis=1)
    row_stds = np.std(gray[:, x_start:x_end], axis=1)
    
    dividers = []
    for y in range(480, h - 140):
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

def process_file_dividers(fpath):
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
        lines.append({'text': text.strip(), 'ymin': ymin, 'ymax': ymax})
        
    dividers = find_dividers(img)
    if not dividers:
        return []
        
    crops = []
    for i in range(len(dividers) - 1):
        y_top = dividers[i]
        y_bot = dividers[i+1]
        
        # Find SKU in this vertical range
        sku = ''
        upc = ''
        row_lines = [l for l in lines if y_top - 20 <= l['ymin'] and l['ymax'] <= y_bot + 20]
        
        for l in row_lines:
            t = l['text']
            if 'SKU' in t.upper():
                sku_m = re.search(r'SKU\s*[:：]?\s*(\d+)', t, re.IGNORECASE)
                if sku_m:
                    sku = sku_m.group(1)
                upc_m = re.search(r'UPC\s*[:：]?\s*(\d+)', t, re.IGNORECASE)
                if upc_m:
                    upc = upc_m.group(1)
                    
        if not sku:
            continue
            
        # Crop bottle from this exact row
        sub = img[int(y_top + 6):int(y_bot - 6), int(w * 0.04):int(w * 0.28)]
        if sub.size == 0:
            continue
            
        gray = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
        mask = gray < 246
        coords = np.argwhere(mask)
        if len(coords) < 100:
            continue
            
        cy0, cx0 = coords.min(axis=0)
        cy1, cx1 = coords.max(axis=0)
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
                'upc': upc,
                'crop': cropped_drink,
                'height': ch,
                'width': cw,
                'file': os.path.basename(fpath)
            })
            
    return crops

if __name__ == '__main__':
    files = sorted(glob.glob('Screenshot_*.jpg'))
    print(f'Extracting perfect divider crops from {len(files)} files...')
    with Pool(2) as pool:
        all_res = pool.map(process_file_dividers, files)
        
    flat = []
    for r in all_res:
        flat.extend(r)
        
    print(f'Total divider crops: {len(flat)}')
    
    by_sku = {}
    for item in flat:
        sku = item['sku']
        if sku not in by_sku or item['height'] > by_sku[sku]['height']:
            by_sku[sku] = item
            
    print(f'Unique SKUs with perfect crops: {len(by_sku)}')
    
    os.makedirs('drink_images', exist_ok=True)
    for sku, item in by_sku.items():
        out_path = f"drink_images/sku_{sku}.png"
        cv2.imwrite(out_path, item['crop'])
        
    print('All perfect crops saved to drink_images/')
