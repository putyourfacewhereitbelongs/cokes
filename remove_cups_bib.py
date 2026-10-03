import json

with open('public/data/drinks.json') as f:
    drinks = json.load(f)

# Filter out cups and bag-in-box / bagged boxed drinks
filtered_drinks = []
for d in drinks:
    name_l = d['full_name'].lower()
    cat_l = d['category'].lower()
    ctype_l = d['container_type'].lower()
    brand_l = d['brand_group'].lower()
    pack_l = (d['packaging'] or '').lower()
    
    is_cup = 'cup' in name_l or 'cup' in cat_l or 'cup' in ctype_l or 'cup' in brand_l
    is_bib = 'bag-in-box' in name_l or 'bag-in-box' in cat_l or 'bag-in-box' in ctype_l or 'bag-in-box' in brand_l or 'bag-in-box' in pack_l or 'bagged' in name_l or 'box' in ctype_l or 'syrup' in name_l or 'beverage mix' in name_l or 'beverage component' in name_l
    
    if not is_cup and not is_bib:
        filtered_drinks.append(d)

print(f"Original drinks: {len(drinks)} -> Filtered drinks: {len(filtered_drinks)}")

# Re-index row numbers
for i, d in enumerate(filtered_drinks):
    d['row_num'] = i + 1

with open('public/data/drinks.json', 'w') as f:
    json.dump(filtered_drinks, f, indent=2)

print("Updated public/data/drinks.json successfully!")
