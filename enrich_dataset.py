import json
import re

with open('final_drinks_master.json') as f:
    items = json.load(f)

# Planogram Cooler Door mapping for training
door_mapping = {
    'Coca-Cola': 'Door 1: Core Colas & Classic Soft Drinks',
    'Diet Coke': 'Door 1: Core Colas & Classic Soft Drinks',
    'Sprite': 'Door 2: Lemon-Lime, Pepper & Flavors',
    'Dr Pepper': 'Door 2: Lemon-Lime, Pepper & Flavors',
    'Fanta': 'Door 2: Lemon-Lime, Pepper & Flavors',
    'Mello Yello': 'Door 2: Lemon-Lime, Pepper & Flavors',
    "Barq's Root Beer": 'Door 2: Lemon-Lime, Pepper & Flavors',
    "Seagram's Ginger Ale": 'Door 2: Lemon-Lime, Pepper & Flavors',
    'Monster Energy': 'Door 3: Monster Energy & Nitro',
    'Monster Energy Ultra': 'Door 3: Monster Energy & Nitro',
    'Monster Energy Juice': 'Door 3: Monster Energy & Nitro',
    'Monster Rehab': 'Door 3: Monster Energy & Nitro',
    'Java Monster Coffee': 'Door 7: RTD Coffee, Dairy & Protein',
    'Reign Total Body Fuel': 'Door 4: Performance Energy (Reign, Bang, NOS)',
    'Bang Energy': 'Door 4: Performance Energy (Reign, Bang, NOS)',
    'NOS Energy': 'Door 4: Performance Energy (Reign, Bang, NOS)',
    'Full Throttle': 'Door 4: Performance Energy (Reign, Bang, NOS)',
    'Storm Energy': 'Door 4: Performance Energy (Reign, Bang, NOS)',
    'Powerade': 'Door 5: Sports Drinks & Hydration',
    'Powerade Power Water': 'Door 5: Sports Drinks & Hydration',
    'BODYARMOR SuperDrink & Lyte': 'Door 5: Sports Drinks & Hydration',
    'BODYARMOR Flash I.V.': 'Door 5: Sports Drinks & Hydration',
    'BODYARMOR Fit': 'Door 5: Sports Drinks & Hydration',
    'BODYARMOR SportWater': 'Door 6: Enhanced Water & Wellness',
    'smartwater': 'Door 6: Enhanced Water & Wellness',
    'vitaminwater': 'Door 6: Enhanced Water & Wellness',
    'Dasani Water': 'Door 6: Enhanced Water & Wellness',
    'Topo Chico': 'Door 6: Enhanced Water & Wellness',
    'Minute Maid': 'Door 7: Juices, Teas, Coffee & Dairy',
    'Hi-C': 'Door 7: Juices, Teas, Coffee & Dairy',
    'Gold Peak Tea': 'Door 7: Juices, Teas, Coffee & Dairy',
    'Fairlife Milk': 'Door 7: Juices, Teas, Coffee & Dairy',
    'Core Power Protein': 'Door 7: Juices, Teas, Coffee & Dairy',
    "Dunkin' Iced Coffee": 'Door 7: Juices, Teas, Coffee & Dairy',
    'Tum-E Yummies': 'Door 7: Juices, Teas, Coffee & Dairy',
    'Bag-in-Box Syrups': 'Backroom / Fountain Dispenser Station',
    'Bag-in-Box Mixes': 'Backroom / Fountain Dispenser Station',
    'Cups & Supplies': 'Fountain Drink Counter',
}

# Velocity / Best seller tags
top_sellers_skus = {
    '102603', '102604', '101891', '117635', '121751', '119790', '133129', '145105',
    '153389', '156834', '156843', '412515', '412520', '129252', '116366', '151817',
    '151818', '156184', '135333', '152013', '152923', '412555', '410704', '152196',
    '132530', '132540', '132606', '115583', '115584', '115586', '117603', '413936'
}

for d in items:
    sku = d['sku']
    brand = d['brand_group']
    name = d['full_name']
    
    d['image_path'] = f"drinks/{sku}.png"
    d['cooler_zone'] = door_mapping.get(brand, 'Cooler Floor Display')
    d['is_best_seller'] = sku in top_sellers_skus
    
    # Nutritional / feature badges
    tags = []
    if 'Zero Sugar' in name or 'Zero' in name or 'Diet' in name:
        tags.append('Zero Sugar')
    if 'Protein' in name or 'Elite' in name or '26g' in name or '42g' in name:
        tags.append('High Protein')
    if 'Energy' in d['category'] or 'Energy' in name or 'Nitro' in name or 'Coffee' in name:
        tags.append('Energy / Caffeine')
    if 'Electrolytes' in name or 'Sports' in d['category'] or 'Hydration' in d['category'] or 'Flash I.V.' in name:
        tags.append('Electrolytes')
    if 'Mexico' in name or 'Glass' in d['container_type']:
        tags.append('Real Cane Sugar (Mexico)')
    if '100%' in name or 'Juice' in name:
        tags.append('Juice')
    if 'Tea' in name:
        tags.append('Real Brewed')
    if 'Alkaline' in name:
        tags.append('Alkaline Water')
        
    d['tags'] = tags

with open('public/data/drinks.json', 'w') as f:
    json.dump(items, f, indent=2)

print(f"Master drinks saved to public/data/drinks.json with {len(items)} items!")
