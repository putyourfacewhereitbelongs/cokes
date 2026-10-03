import json
import re

with open('products_to_review.json') as f:
    products = json.load(f)

def clean_and_categorize(p):
    raw = p['raw_cleaned']
    sku = p['sku']
    upc = p['upc']
    
    # Clean up common OCR merging/spaces
    text = raw
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Specific known fixes based on OCR
    # Let's handle special SKU cases
    custom_overrides = {
        '151817': ('Dairy & Protein Drinks', 'Core Power', 'Core Power Protein Chocolate Elite 42G', '14 oz', 'Plastic Bottle', '12 Loose'),
        '150885': ('Energy Drinks', 'Monster Rehab', 'Monster Rehab Tea + Peach', '15.5 oz', 'Can', '24 Loose'),
        '138036': ('Energy Drinks', 'Monster Rehab', 'Monster Rehab Tea + Lemonade', '15.5 oz', 'Can', '24 Loose'),
        '412029': ('Energy Drinks', 'Monster Rehab', 'Monster Rehab Tea + Lemonade', '18.6 oz', 'Can', '12 Loose'),
        '700015': ('Fountain & Supplies', 'Cups & Supplies', 'Cups 12 oz Styrofoam TB', '12 oz', 'Cup', 'Case'),
        '116965': ('Fountain & Supplies', 'Cups & Supplies', 'Cups 16 oz Styrofoam', '16 oz', 'Cup', 'Case'),
        '144892': ('Fountain & Supplies', 'Cups & Supplies', 'Cups 12 oz Paper Trademark', '12 oz', 'Cup', '2000 Count'),
        '144893': ('Fountain & Supplies', 'Cups & Supplies', 'Cups 16 oz Paper Trademark', '16 oz', 'Cup', '1000 Count'),
        '151208': ('Fountain & Supplies', 'Bag-in-Box Mixes', 'Coca-Cola Md Beverage Mix', '46 oz', 'Bag-in-Box', 'Box'),
        '151215': ('Fountain & Supplies', 'Bag-in-Box Mixes', 'Barqs / Diet Barqs Md Beverage Mix', '46 oz', 'Bag-in-Box', 'Box'),
        '151218': ('Fountain & Supplies', 'Bag-in-Box Mixes', 'Minute Maid Lemonade / Light Md Beverage Component', '34 oz', 'Bag-in-Box', 'Box'),
        '412321': ('Fountain & Supplies', 'Bag-in-Box Mixes', 'Seagrams Ginger Ale / Zero Sugar Ginger Ale Md Beverage Mix', '36 oz', 'Bag-in-Box', 'Box'),
        '412322': ('Fountain & Supplies', 'Bag-in-Box Mixes', 'Mello Yello / Mello Yello Zero Md Beverage Mix', '36 oz', 'Bag-in-Box', 'Box'),
        '150932': ('Fountain & Supplies', 'Bag-in-Box Mixes', 'Powerade Md Beverage Component', '23 oz', 'Bag-in-Box', 'Box'),
        '152098': ('Fountain & Supplies', 'Bag-in-Box Mixes', 'Glaceau Vitaminwater Md Beverage Component', '11.5 oz', 'Bag-in-Box', 'Box'),
        '104235': ('Fountain & Supplies', 'Bag-in-Box Syrups', 'Barqs Root Beer Bag-in-Box Syrup', '2.5 Gal', 'Bag-in-Box', '1 Box'),
        '104148': ('Fountain & Supplies', 'Bag-in-Box Syrups', 'Hi-C Fruit Punch Bag-in-Box Syrup', '2.5 Gal', 'Bag-in-Box', '1 Box'),
        '103895': ('Fountain & Supplies', 'Bag-in-Box Syrups', 'Hi-C Pink Lemonade Bag-in-Box Syrup', '2.5 Gal', 'Bag-in-Box', '1 Box'),
        '109147': ('Fountain & Supplies', 'Bag-in-Box Syrups', 'Minute Maid Lemonade Bag-in-Box Syrup', '2.5 Gal', 'Bag-in-Box', '1 Box'),
        '104239': ('Fountain & Supplies', 'Bag-in-Box Syrups', 'Powerade Mountain Blast Bag-in-Box Syrup', '2.5 Gal', 'Bag-in-Box', '1 Box'),
        '132766': ('Fountain & Supplies', 'Bag-in-Box Syrups', 'Gold Peak Premium Unsweetened Tea Bag-in-Box Syrup', '2.5 Gal', 'Bag-in-Box', '1 Box'),
        '139200': ('Fountain & Supplies', 'Bag-in-Box Syrups', 'Gold Peak Southern Style Tea Bag-in-Box Syrup', '5 Gal', 'Bag-in-Box', '1 Box'),
    }
    
    if sku in custom_overrides:
        cat, subcat, full_name, size, ctype, pack = custom_overrides[sku]
        return {
            'sku': sku,
            'upc': upc,
            'category': cat,
            'brand_group': subcat,
            'full_name': full_name,
            'size': size,
            'container_type': ctype,
            'packaging': pack,
            'image_path': f'drink_images/sku_{sku}.png',
            'raw': raw
        }
    
    # Parse Size
    size_match = re.search(r'(\d+(?:\.\d+)?\s*(?:oz|ltr|Itr|liter|L|gal|ml|g|G))\b', text, re.IGNORECASE)
    size = size_match.group(1) if size_match else ''
    # Normalize size string
    size = re.sub(r'(?i)itr', 'Liter', size)
    size = re.sub(r'(?i)ltr', 'Liter', size)
    size = re.sub(r'(?i)2\s*Liter', '2 Liter', size)
    size = re.sub(r'(?i)1\s*Liter', '1 Liter', size)
    size = re.sub(r'(?i)1\.5\s*Liter', '1.5 Liter', size)
    size = re.sub(r'(?i)oz', 'oz', size)
    size = re.sub(r'(?i)ml', 'mL', size)
    
    # Parse Packaging
    pack = ''
    if re.search(r'12\s*pk\s*,\s*2\s*ct', text, re.IGNORECASE) or '12 pk, 2 ct' in text or '12 pk,2 ct' in text or '12pk,2ct' in text:
        pack = '12 Pack (2 CT)'
    elif re.search(r'15\s*pk\s*,\s*2\s*ct', text, re.IGNORECASE) or '15 pk, 2 ct' in text or '15 pk,2 ct' in text:
        pack = '15 Pack (2 CT)'
    elif re.search(r'6\s*pk\s*,\s*4\s*ct', text, re.IGNORECASE) or '6 pk, 4 ct' in text or '6 pk,4 ct' in text:
        pack = '6 Pack (4 CT)'
    elif re.search(r'4\s*pk\s*,\s*6\s*ct', text, re.IGNORECASE) or '4 pk, 6 ct' in text or '4 pk,6 ct' in text:
        pack = '4 Pack (6 CT)'
    elif re.search(r'8\s*pk', text, re.IGNORECASE):
        pack = '8 Pack'
    elif re.search(r'24\s*pk', text, re.IGNORECASE):
        pack = '24 Pack Case'
    elif re.search(r'24\s*(?:loose|lo0se)', text, re.IGNORECASE):
        pack = '24 Loose'
    elif re.search(r'12\s*(?:loose|lo0se)', text, re.IGNORECASE):
        pack = '12 Loose'
    elif re.search(r'15\s*(?:loose|lo0se)', text, re.IGNORECASE):
        pack = '15 Loose'
    elif re.search(r'8\s*(?:loose|lo0se)', text, re.IGNORECASE):
        pack = '8 Loose'
    elif 'bag-in-box' in text.lower():
        pack = 'Bag-in-Box'
    elif 'loose' in text.lower() or 'lo0se' in text.lower():
        pack = 'Loose'
        
    # Container type
    ctype = 'Bottle'
    if 'can' in text.lower() or 'cans' in text.lower():
        ctype = 'Can'
    elif 'bag-in-box' in text.lower():
        ctype = 'Bag-in-Box'
    elif 'glass' in text.lower() or 'mexico' in text.lower() or '355' in text or '8 oz bottle' in text.lower():
        ctype = 'Glass Bottle'
    elif 'bottle' in text.lower() or 'bottles' in text.lower():
        ctype = 'Plastic Bottle'
    elif 'cup' in text.lower():
        ctype = 'Cup'
        
    # Extract Drink Name before the size/packaging part
    # Look for the brand & flavor
    # We can clean text up to size
    name_part = text
    if size_match:
        idx = size_match.start()
        # Look if there is a comma before size
        prefix = text[:idx].strip()
        prefix = re.sub(r'[,.\-_:;]+$', '', prefix).strip()
        if len(prefix) > 2:
            name_part = prefix
            
    # Clean up name_part
    name_part = re.sub(r'([a-z])([A-Z])', r'\1 \2', name_part)
    name_part = re.sub(r'Coca - Cola', 'Coca-Cola', name_part)
    name_part = re.sub(r'Coca Cola', 'Coca-Cola', name_part)
    name_part = re.sub(r'Diet Coke', 'Diet Coke', name_part)
    name_part = re.sub(r'Dr Pepper', 'Dr Pepper', name_part)
    name_part = re.sub(r'DrPepper', 'Dr Pepper', name_part)
    name_part = re.sub(r'Diet Cherry Coke', 'Diet Cherry Coke', name_part)
    name_part = re.sub(r'Barqs', "Barq's", name_part)
    name_part = re.sub(r"Barq's Root Beer", "Barq's Root Beer", name_part)
    name_part = re.sub(r'Mello Yello', 'Mello Yello', name_part)
    name_part = re.sub(r'MelloYello', 'Mello Yello', name_part)
    name_part = re.sub(r'Seagrams', "Seagram's", name_part)
    name_part = re.sub(r'Glaceau Smartwater', 'smartwater', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Glaceau Vitaminwater', 'vitaminwater', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Glaceausmartwater', 'smartwater', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Glaceauvitaminwater', 'vitaminwater', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Minute Maid', 'Minute Maid', name_part)
    name_part = re.sub(r'MinuteMaid', 'Minute Maid', name_part)
    name_part = re.sub(r'Powerade', 'Powerade', name_part)
    name_part = re.sub(r'Bodyarmor', 'BODYARMOR', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Reign Total Body Fuel', 'Reign Total Body Fuel', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'ReignTotalBodyFuel', 'Reign Total Body Fuel', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Bang Energy', 'Bang Energy', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'BangEnergy', 'Bang Energy', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Monster Energy', 'Monster Energy', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'MonsterEnergy', 'Monster Energy', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Gold Peak', 'Gold Peak', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'GoldPeak', 'Gold Peak', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Fairlife Milk', 'Fairlife Milk', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'FairlifeMilk', 'Fairlife Milk', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Core Power', 'Core Power', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'CorePower', 'Core Power', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r"Dunkin'", "Dunkin'", name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Topo Chico', 'Topo Chico', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Tum - E Yummies', 'Tum-E Yummies', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Tum - E', 'Tum-E', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Tum-EYummies', 'Tum-E Yummies', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Storm Zero Sugar', 'Storm Zero Sugar', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'StormZeroSugar', 'Storm Zero Sugar', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Nos Energy', 'NOS Energy', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Nos', 'NOS', name_part)
    name_part = re.sub(r'Full Throttle', 'Full Throttle', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'FullThrottle', 'Full Throttle', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Dasani', 'Dasani', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Hi - C', 'Hi-C', name_part, flags=re.IGNORECASE)
    name_part = re.sub(r'Hi-C', 'Hi-C', name_part, flags=re.IGNORECASE)
    
    # Clean ellipses
    name_part = re.sub(r'[\.]{2,}', '', name_part).strip()
    
    # Categorization and Brand Group logic
    brand_group = 'Other'
    cat = 'Other Beverages'
    
    lower = name_part.lower() + " " + text.lower()
    
    if 'coca-cola' in lower or 'coca cola' in lower or 'diet cherry coke' in lower:
        cat = 'Carbonated Soft Drinks'
        brand_group = 'Coca-Cola'
    elif 'diet coke' in lower:
        cat = 'Carbonated Soft Drinks'
        brand_group = 'Diet Coke'
    elif 'sprite' in lower:
        cat = 'Carbonated Soft Drinks'
        brand_group = 'Sprite'
    elif 'dr pepper' in lower or 'drpepper' in lower:
        cat = 'Carbonated Soft Drinks'
        brand_group = 'Dr Pepper'
    elif 'fanta' in lower:
        cat = 'Carbonated Soft Drinks'
        brand_group = 'Fanta'
    elif 'mello yello' in lower:
        cat = 'Carbonated Soft Drinks'
        brand_group = 'Mello Yello'
    elif 'barq' in lower:
        cat = 'Carbonated Soft Drinks'
        brand_group = "Barq's Root Beer"
    elif 'seagram' in lower:
        cat = 'Carbonated Soft Drinks'
        brand_group = "Seagram's Ginger Ale"
    elif 'monster' in lower or 'java monster' in lower or 'mega monster' in lower:
        cat = 'Energy Drinks'
        if 'java monster' in lower:
            brand_group = 'Java Monster Coffee'
        elif 'rehab' in lower:
            brand_group = 'Monster Rehab'
        elif 'ultra' in lower:
            brand_group = 'Monster Energy Ultra'
        elif 'juice' in lower:
            brand_group = 'Monster Energy Juice'
        else:
            brand_group = 'Monster Energy'
    elif 'reign' in lower:
        cat = 'Energy Drinks'
        brand_group = 'Reign Total Body Fuel'
    elif 'bang energy' in lower or 'bang' in lower:
        cat = 'Energy Drinks'
        brand_group = 'Bang Energy'
    elif 'nos' in lower:
        cat = 'Energy Drinks'
        brand_group = 'NOS Energy'
    elif 'full throttle' in lower:
        cat = 'Energy Drinks'
        brand_group = 'Full Throttle'
    elif 'storm' in lower:
        cat = 'Energy Drinks'
        brand_group = 'Storm Energy'
    elif 'powerade' in lower:
        if 'power water' in lower:
            cat = 'Sports & Enhanced Water'
            brand_group = 'Powerade Power Water'
        else:
            cat = 'Sports & Hydration'
            brand_group = 'Powerade'
    elif 'bodyarmor' in lower:
        if 'flash' in lower:
            cat = 'Sports & Hydration'
            brand_group = 'BODYARMOR Flash I.V.'
        elif 'fit' in lower:
            cat = 'Sports & Hydration'
            brand_group = 'BODYARMOR Fit'
        elif 'sportwater' in lower:
            cat = 'Bottled & Enhanced Water'
            brand_group = 'BODYARMOR SportWater'
        else:
            cat = 'Sports & Hydration'
            brand_group = 'BODYARMOR SuperDrink & Lyte'
    elif 'smartwater' in lower:
        cat = 'Bottled & Enhanced Water'
        brand_group = 'smartwater'
    elif 'vitaminwater' in lower:
        cat = 'Enhanced Water & Wellness'
        brand_group = 'vitaminwater'
    elif 'dasani' in lower:
        cat = 'Bottled & Enhanced Water'
        brand_group = 'Dasani Water'
    elif 'topo chico' in lower:
        cat = 'Sparkling Water & Seltzers'
        brand_group = 'Topo Chico'
    elif 'minute maid' in lower:
        cat = 'Juices & Fruit Drinks'
        brand_group = 'Minute Maid'
    elif 'hi-c' in lower:
        cat = 'Juices & Fruit Drinks'
        brand_group = 'Hi-C'
    elif 'gold peak' in lower:
        cat = 'Ready-to-Drink Teas'
        brand_group = 'Gold Peak Tea'
    elif 'core power' in lower:
        cat = 'Dairy & Protein Drinks'
        brand_group = 'Core Power Protein'
    elif 'fairlife' in lower:
        cat = 'Dairy & Protein Drinks'
        brand_group = 'Fairlife Milk'
    elif 'dunkin' in lower:
        cat = 'Ready-to-Drink Coffee'
        brand_group = "Dunkin' Iced Coffee"
    elif 'tum-e' in lower or 'tum - e' in lower:
        cat = 'Kids Drinks & Juices'
        brand_group = 'Tum-E Yummies'
    elif 'cup' in lower:
        cat = 'Fountain & Supplies'
        brand_group = 'Cups & Supplies'
        
    return {
        'sku': sku,
        'upc': upc,
        'category': cat,
        'brand_group': brand_group,
        'full_name': name_part,
        'size': size if size else '',
        'container_type': ctype,
        'packaging': pack if pack else '',
        'image_path': f'drink_images/sku_{sku}.png',
        'raw': raw
    }

parsed = [clean_and_categorize(p) for p in products]

with open('parsed_drinks.json', 'w') as f:
    json.dump(parsed, f, indent=2)

print(f"Parsed {len(parsed)} drinks successfully!")
