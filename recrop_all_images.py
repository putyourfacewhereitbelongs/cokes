import cv2
import numpy as np
import glob
import os
import json
import re

def find_dividers(img):
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x_start = int(w * 0.1)
    x_end = int(w * 0.9)
    row_means = np.mean(gray[:, x_start:x_end], axis=1)
    row_stds = np.std(gray[:, x_start:x_end], axis=1)
    
    dividers = []
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

def clean_crop_bottle(img, y_top, y_bot, w):
    x0 = int(w * 0.04)
    x1 = int(w * 0.28)
    sub = img[int(y_top + 6):int(y_bot - 6), x0:x1]
    if sub.size == 0:
        return None
    gray = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY)
    mask = gray < 246
    coords = np.argwhere(mask)
    if len(coords) < 100:
        return None
    cy0, cx0 = coords.min(axis=0)
    cy1, cx1 = coords.max(axis=0)
    pad = 4
    cy0 = max(0, cy0 - pad)
    cy1 = min(sub.shape[0], cy1 + pad)
    cx0 = max(0, cx0 - pad)
    cx1 = min(sub.shape[1], cx1 + pad)
    return sub[cy0:cy1, cx0:cx1]

with open('all_detailed_products.json') as f:
    products = json.load(f)

# Group products by source file
by_file = {}
for p in products:
    f = p['file']
    if f not in by_file:
        by_file[f] = []
    by_file[f].append(p)

os.makedirs('drink_images', exist_ok=True)
best_crops = {}

for f, file_prods in by_file.items():
    img = cv2.imread(f)
    if img is None:
        continue
    h, w = img.shape[:2]
    dividers = find_dividers(img)
    
    # Sort file_prods by SKU or order in file
    # We can match each product in file_prods to dividers
    # Since products are in top-to-bottom order in the file:
    # If there are N products and M dividers:
    for i, p in enumerate(file_prods):
        sku = p['sku']
        if not sku:
            continue
        
        # Find divider interval for this product
        # Look around product SKU line position or approximate row
        # In general, if there are K dividers:
        # A row is between divider[k] and divider[k+1]
        best_crop = None
        max_h = 0
        
        # Test all divider intervals in this file that match the rough vertical span
        for k in range(len(dividers) - 1):
            y_t = dividers[k]
            y_b = dividers[k+1]
            if 200 < (y_b - y_t) < 700:
                crop = clean_crop_bottle(img, y_t, y_b, w)
                if crop is not None:
                    # Check if this interval corresponds to this product index i
                    # If i < len(dividers)-1 and dividers[i] == y_t:
                    pass
        
        # Let's directly match row i to divider pair i -> i+1 if length matches
        # Or search for the divider pair around index i
        if len(dividers) >= len(file_prods) + 1:
            # First divider is above first product
            y_t = dividers[i]
            y_b = dividers[i+1]
            crop = clean_crop_bottle(img, y_t, y_b, w)
            if crop is not None and crop.shape[0] > max_h:
                best_crop = crop
                max_h = crop.shape[0]
        else:
            # Fallback estimation
            y_approx_start = 550 + i * 480
            y_approx_end = y_approx_start + 480
            crop = clean_crop_bottle(img, y_approx_start, y_approx_end, w)
            if crop is not None and crop.shape[0] > max_h:
                best_crop = crop
                max_h = crop.shape[0]
                
        if best_crop is not None:
            if sku not in best_crops or max_h > best_crops[sku][0]:
                best_crops[sku] = (max_h, best_crop)

print(f"Recropped {len(best_crops)} SKUs cleanly!")

for sku, (ch, crop) in best_crops.items():
    out_p = f"drink_images/sku_{sku}.png"
    cv2.imwrite(out_p, crop)

print("Saved all clean crops to drink_images/")
