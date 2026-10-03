import json
import re

with open('all_detailed_products.json') as f:
    items = json.load(f)

by_sku = {}
for it in items:
    sku = it['sku']
    if sku not in by_sku:
        by_sku[sku] = []
    by_sku[sku].append(it)

print(f"Total unique SKUs to normalize: {len(by_sku)}")

cleaned_products = []

for sku, entries in by_sku.items():
    # Find entry with best name and tallest crop
    best_entry = max(entries, key=lambda x: (len(re.sub(r'[\+\-\×\中\十\s]', '', x['raw_name'])), x['crop_h']))
    upc = ''
    for e in entries:
        if e['upc'] and len(e['upc']) >= 8:
            upc = e['upc']
            break
            
    raw = best_entry['raw_name']
    
    # Clean OCR artefacts from raw
    cleaned = raw
    cleaned = re.sub(r'^(Add\s*to\s*Cart|AddtoCart|Add toCart|\+|\-|\×|\中|\十|\–|\*)\s*', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s*(Add\s*to\s*Cart|AddtoCart|Add toCart|\+|\-|\×|\中|\十|\–|\*)$', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'^\s*[,.\-_:;]+\s*', '', cleaned)
    cleaned = re.sub(r'\s*[,.\-_:;]+$', '', cleaned)
    
    cleaned_products.append({
        'sku': sku,
        'upc': upc,
        'raw_cleaned': cleaned,
        'original_raw': raw,
        'crop_h': best_entry['crop_h'],
        'crop_w': best_entry['crop_w'],
        'source_file': best_entry['file']
    })

cleaned_products.sort(key=lambda x: x['sku'])

with open('products_to_review.json', 'w') as f:
    json.dump(cleaned_products, f, indent=2)

print("Saved products_to_review.json")
