import json
import re

with open('all_detailed_products.json') as f:
    items = json.load(f)

# Deduplicate by SKU, taking the richest entry
by_sku = {}
for it in items:
    sku = it['sku']
    if not sku:
        continue
    if sku not in by_sku:
        by_sku[sku] = []
    by_sku[sku].append(it)

print(f"Total unique SKUs: {len(by_sku)}")

def parse_entry(sku, entries):
    # Find entry with best crop and text
    best = max(entries, key=lambda x: (x['crop_h'], len(''.join(x['title_lines']))))
    upc = ''
    for e in entries:
        if e['upc'] and len(e['upc']) >= 8:
            upc = e['upc']
            break
            
    # Combine title lines from all entries to get fullest text
    all_lines = []
    for e in entries:
        for l in e['title_lines']:
            cl = re.sub(r'^(Add\s*to\s*Cart|AddtoCart|Add toCart|\+|\-|\×|\中|\十|\–|\*)\s*', '', l, flags=re.IGNORECASE).strip()
            cl = re.sub(r'\s*(Add\s*to\s*Cart|AddtoCart|Add toCart|\+|\-|\×|\中|\十|\–|\*)$', '', cl, flags=re.IGNORECASE).strip()
            if cl and cl not in all_lines:
                all_lines.append(cl)
                
    raw_joined = ' '.join(best['title_lines'])
    raw_joined = re.sub(r'^(Add\s*to\s*Cart|AddtoCart|Add toCart|\+|\-|\×|\中|\十|\–|\*)\s*', '', raw_joined, flags=re.IGNORECASE)
    raw_joined = re.sub(r'\s*(Add\s*to\s*Cart|AddtoCart|Add toCart|\+|\-|\×|\中|\十|\–|\*)$', '', raw_joined, flags=re.IGNORECASE)
    raw_joined = re.sub(r'^\s*[,.\-_:;]+\s*', '', raw_joined)
    raw_joined = re.sub(r'\s*[,.\-_:;]+$', '', raw_joined)

    # Insert spaces between camelCase and numbers
    text = raw_joined
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Custom Overrides
    custom = {
        '151817': ('Dairy & Protein Drinks', 'Core Power Protein', 'Core Power Protein Chocolate Elite 42g', '14 oz', 'Plastic Bottle', '12 Loose'),
        '150885': ('Energy Drinks', 'Monster Rehab', 'Monster Rehab Tea + Peach', '15.5 oz', 'Can', '24 Loose'),
        '138036': ('Energy Drinks', 'Monster Rehab', 'Monster Rehab Tea + Lemonade', '15.5 oz', 'Can', '24 Loose'),
        '412029': ('Energy Drinks', 'Monster Rehab', 'Monster Rehab Tea + Lemonade', '18.6 oz', 'Can', '12 Loose'),
        '700015': ('Fountain & Supplies', 'Cups & Supplies', 'Cups 12 oz Styrofoam TB', '12 oz', 'Cup', 'Case'),
        '116965': ('Fountain & Supplies', 'Cups & Supplies', 'Cups 16 oz Styrofoam', '16 oz', 'Cup', 'Case'),
        '144892': ('Fountain & Supplies', 'Cups & Supplies', 'Cups 12 oz Paper Trademark', '12 oz', 'Cup', '2000 Count'),
        '144893': ('Fountain & Supplies', 'Cups & Supplies', 'Cups 16 oz Paper Trademark', '16 oz', 'Cup', '1000 Count'),
        '151208': ('Fountain & Supplies', 'Bag-in-Box Mixes', 'Coca-Cola Md Beverage Mix', '46 oz', 'Bag-in-Box', '1 Box'),
        '151215': ('Fountain & Supplies', 'Bag-in-Box Mixes', 'Barqs / Diet Barqs Md Beverage Mix', '46 oz', 'Bag-in-Box', '1 Box'),
        '151218': ('Fountain & Supplies', 'Bag-in-Box Mixes', 'Minute Maid Lemonade / Light Md Beverage Component', '34 oz', 'Bag-in-Box', '1 Box'),
        '412321': ('Fountain & Supplies', 'Bag-in-Box Mixes', 'Seagrams Ginger Ale / Zero Sugar Ginger Ale Md Beverage Mix', '36 oz', 'Bag-in-Box', '1 Box'),
        '412322': ('Fountain & Supplies', 'Bag-in-Box Mixes', 'Mello Yello / Mello Yello Zero Md Beverage Mix', '36 oz', 'Bag-in-Box', '1 Box'),
        '150932': ('Fountain & Supplies', 'Bag-in-Box Mixes', 'Powerade Md Beverage Component', '23 oz', 'Bag-in-Box', '1 Box'),
        '152098': ('Fountain & Supplies', 'Bag-in-Box Mixes', 'Glaceau Vitaminwater Md Beverage Component', '11.5 oz', 'Bag-in-Box', '1 Box'),
        '104235': ('Fountain & Supplies', 'Bag-in-Box Syrups', 'Barqs Root Beer Bag-in-Box Syrup', '2.5 Gal', 'Bag-in-Box', '1 Box'),
        '104148': ('Fountain & Supplies', 'Bag-in-Box Syrups', 'Hi-C Fruit Punch Bag-in-Box Syrup', '2.5 Gal', 'Bag-in-Box', '1 Box'),
        '103895': ('Fountain & Supplies', 'Bag-in-Box Syrups', 'Hi-C Pink Lemonade Bag-in-Box Syrup', '2.5 Gal', 'Bag-in-Box', '1 Box'),
        '109147': ('Fountain & Supplies', 'Bag-in-Box Syrups', 'Minute Maid Lemonade Bag-in-Box Syrup', '2.5 Gal', 'Bag-in-Box', '1 Box'),
        '104239': ('Fountain & Supplies', 'Bag-in-Box Syrups', 'Powerade Mountain Blast Bag-in-Box Syrup', '2.5 Gal', 'Bag-in-Box', '1 Box'),
        '132766': ('Fountain & Supplies', 'Bag-in-Box Syrups', 'Gold Peak Premium Unsweetened Tea Bag-in-Box Syrup', '2.5 Gal', 'Bag-in-Box', '1 Box'),
        '139200': ('Fountain & Supplies', 'Bag-in-Box Syrups', 'Gold Peak Southern Style Tea Bag-in-Box Syrup', '5 Gal', 'Bag-in-Box', '1 Box'),
        '156188': ('Dairy & Protein Drinks', 'Core Power Protein', 'Core Power Protein Strawberry Banana 26g', '14 oz', 'Plastic Bottle', '12 Loose'),
        '157128': ('Dairy & Protein Drinks', 'Core Power Protein', 'Core Power Protein Strawberry Elite 42g', '14 oz', 'Plastic Bottle', '12 Loose'),
        '156182': ('Dairy & Protein Drinks', 'Core Power Protein', 'Core Power Protein Vanilla 26g', '14 oz', 'Plastic Bottle', '12 Loose'),
        '151818': ('Dairy & Protein Drinks', 'Core Power Protein', 'Core Power Protein Vanilla Elite 42g', '14 oz', 'Plastic Bottle', '12 Loose'),
        '156184': ('Dairy & Protein Drinks', 'Core Power Protein', 'Core Power Protein Chocolate 26g', '14 oz', 'Plastic Bottle', '12 Loose'),
        '410721': ('Dairy & Protein Drinks', 'Fairlife Milk', 'Fairlife 2% Chocolate Ultra-Filtered Milk', '14 oz', 'Plastic Bottle', '12 Loose'),
        '411523': ('Dairy & Protein Drinks', 'Fairlife Milk', 'Fairlife 2% Reduced Fat Ultra-Filtered Milk', '14 oz', 'Plastic Bottle', '12 Loose'),
        '411524': ('Dairy & Protein Drinks', 'Fairlife Milk', 'Fairlife 2% Strawberry Ultra-Filtered Milk', '14 oz', 'Plastic Bottle', '12 Loose'),
        '412451': ('Ready-to-Drink Coffee', "Dunkin' Iced Coffee", "Dunkin' Caramel Iced Coffee", '13.7 oz', 'Plastic Bottle', '12 Loose'),
        '152921': ('Ready-to-Drink Coffee', "Dunkin' Iced Coffee", "Dunkin' French Vanilla Iced Coffee", '13.7 oz', 'Plastic Bottle', '12 Loose'),
        '152922': ('Ready-to-Drink Coffee', "Dunkin' Iced Coffee", "Dunkin' Mocha Iced Coffee", '13.7 oz', 'Plastic Bottle', '12 Loose'),
        '152923': ('Ready-to-Drink Coffee', "Dunkin' Iced Coffee", "Dunkin' Original Iced Coffee", '13.7 oz', 'Plastic Bottle', '12 Loose'),
        '413935': ('Ready-to-Drink Coffee', "Dunkin' Iced Coffee", "Dunkin' Double Espresso - Original", '15 oz', 'Can', '12 Loose'),
        '413616': ('Ready-to-Drink Coffee', "Dunkin' Iced Coffee", "Dunkin' Double Espresso - Cafe Mocha", '15 oz', 'Can', '12 Loose'),
        '412030': ('Energy Drinks', 'Java Monster Coffee', 'Java Monster Cafe Latte', '15 oz', 'Can', '12 Loose'),
        '134923': ('Energy Drinks', 'Java Monster Coffee', 'Java Monster Irish Blend', '15 oz', 'Can', '12 Loose'),
        '134929': ('Energy Drinks', 'Java Monster Coffee', 'Java Monster Loca Moca', '15 oz', 'Can', '12 Loose'),
        '134926': ('Energy Drinks', 'Java Monster Coffee', 'Java Monster Mean Bean', '15 oz', 'Can', '12 Loose'),
        '151811': ('Energy Drinks', 'Java Monster Coffee', 'Java Monster Salted Caramel', '15 oz', 'Can', '12 Loose'),
        '413306': ('Energy Drinks', 'Java Monster Coffee', 'Monster Killer Brew Loca Moca', '15 oz', 'Can', '12 Loose'),
        '413346': ('Energy Drinks', 'Java Monster Coffee', 'Monster Killer Brew Mean Bean', '15 oz', 'Can', '12 Loose'),
        '412588': ('Energy Drinks', 'Monster Rehab', 'Monster Rehab Green Tea + Energy', '15.5 oz', 'Can', '24 Loose'),
        '412182': ('Energy Drinks', 'Monster Rehab', 'Monster Rehab Wild Berry Tea', '15.5 oz', 'Can', '24 Loose'),
    }
    
    if sku in custom:
        cat, brand, name, size, ctype, pack = custom[sku]
        return {
            'sku': sku,
            'upc': upc,
            'category': cat,
            'brand_group': brand,
            'full_name': name,
            'size': size,
            'container_type': ctype,
            'packaging': pack,
            'image_path': f'drink_images/sku_{sku}.png'
        }
        
    # Extract size pattern: e.g. 16.9 oz, 20 oz, 12 oz, 2 Itr, 2 ltr, 2 liter, 2 L, 2.5 gal, 355 ml, 7.5 oz, 8 oz, 24 oz, 28 oz, 1 Itr, 1.5 Itr, 23.7 oz, 10.1 oz, 18.5 oz, 18.6 oz, 19.2 oz
    size_match = re.search(r'(\d+(?:\.\d+)?\s*(?:oz|ltr|Itr|liter|L|gal|ml))\b', text, re.IGNORECASE)
    size_str = ''
    name_str = text
    if size_match:
        size_raw = size_match.group(1)
        name_str = text[:size_match.start()].strip()
        # normalize size
        size_raw = re.sub(r'(?i)itr', 'Liter', size_raw)
        size_raw = re.sub(r'(?i)ltr', 'Liter', size_raw)
        size_raw = re.sub(r'(?i)liter', 'Liter', size_raw)
        size_raw = re.sub(r'(\d+)\s*(?:Liter|L)', r'\1 Liter', size_raw)
        size_raw = re.sub(r'(\d+(?:\.\d+)?)\s*oz', r'\1 oz', size_raw)
        size_raw = re.sub(r'(\d+(?:\.\d+)?)\s*ml', r'\1 mL', size_raw)
        size_raw = re.sub(r'(\d+(?:\.\d+)?)\s*gal', r'\1 Gal', size_raw)
        size_str = size_raw.strip()
    
    # Extract packaging
    pack_str = ''
    if re.search(r'12\s*pk\s*[,，]?\s*2\s*ct', text, re.IGNORECASE):
        pack_str = '12 Pack (2 CT)'
    elif re.search(r'15\s*pk\s*[,，]?\s*2\s*ct', text, re.IGNORECASE):
        pack_str = '15 Pack (2 CT)'
    elif re.search(r'6\s*pk\s*[,，]?\s*4\s*ct', text, re.IGNORECASE):
        pack_str = '6 Pack (4 CT)'
    elif re.search(r'4\s*pk\s*[,，]?\s*6\s*ct', text, re.IGNORECASE):
        pack_str = '4 Pack (6 CT)'
    elif re.search(r'8\s*pk', text, re.IGNORECASE):
        pack_str = '8 Pack'
    elif re.search(r'24\s*pk', text, re.IGNORECASE):
        pack_str = '24 Pack Case'
    elif re.search(r'24\s*(?:loose|lo0se)', text, re.IGNORECASE):
        pack_str = '24 Loose'
    elif re.search(r'12\s*(?:loose|lo0se)', text, re.IGNORECASE):
        pack_str = '12 Loose'
    elif re.search(r'15\s*(?:loose|lo0se)', text, re.IGNORECASE):
        pack_str = '15 Loose'
    elif re.search(r'8\s*(?:loose|lo0se)', text, re.IGNORECASE):
        pack_str = '8 Loose'
    elif 'bag-in-box' in text.lower():
        pack_str = '1 Box'
    elif 'loose' in text.lower():
        pack_str = 'Loose'
        
    # Container type
    ctype = 'Plastic Bottle'
    if 'can' in text.lower():
        ctype = 'Can'
    elif 'bag-in-box' in text.lower():
        ctype = 'Bag-in-Box'
    elif 'cup' in text.lower():
        ctype = 'Cup'
    elif 'mexico' in text.lower() or '355' in text or ('8 oz' in size_str and 'bottle' in text.lower()):
        ctype = 'Glass Bottle'
        
    # Clean up name_str
    name_str = re.sub(r'[,.\-_:;]+$', '', name_str).strip()
    
    # Specific normalization rules for drink names
    name_str = re.sub(r'Coca - Cola', 'Coca-Cola', name_str)
    name_str = re.sub(r'Coca Cola', 'Coca-Cola', name_str)
    name_str = re.sub(r'DrPepper', 'Dr Pepper', name_str)
    name_str = re.sub(r'Dr Pepper', 'Dr Pepper', name_str)
    name_str = re.sub(r'DietDrPepper', 'Diet Dr Pepper', name_str)
    name_str = re.sub(r'Diet DrPepper', 'Diet Dr Pepper', name_str)
    name_str = re.sub(r'Diet Coke', 'Diet Coke', name_str)
    name_str = re.sub(r'DietCherryCoke', 'Diet Cherry Coke', name_str)
    name_str = re.sub(r'Diet Cherry Coke', 'Diet Cherry Coke', name_str)
    name_str = re.sub(r'SpriteChill', 'Sprite Chill', name_str)
    name_str = re.sub(r'Sprite Tropical Mix', 'Sprite Tropical Mix', name_str)
    name_str = re.sub(r'SpriteZeroSugar', 'Sprite Zero Sugar', name_str)
    name_str = re.sub(r'Barqs', "Barq's", name_str)
    name_str = re.sub(r'MelloYello', 'Mello Yello', name_str)
    name_str = re.sub(r'Seagrams', "Seagram's", name_str)
    name_str = re.sub(r'Glaceau Smartwater', 'smartwater', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Glaceau Vitaminwater', 'vitaminwater', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Glaceausmartwater', 'smartwater', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Glaceauvitaminwater', 'vitaminwater', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'MinuteMaid', 'Minute Maid', name_str)
    name_str = re.sub(r'Powerade', 'Powerade', name_str)
    name_str = re.sub(r'Bodyarmor', 'BODYARMOR', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Reign Total Body Fuel', 'Reign Total Body Fuel', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'ReignTotalBodyFuel', 'Reign Total Body Fuel', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Bang Energy', 'Bang Energy', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'BangEnergy', 'Bang Energy', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Monster Energy', 'Monster Energy', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'MonsterEnergy', 'Monster Energy', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Gold Peak', 'Gold Peak', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'GoldPeak', 'Gold Peak', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Fairlife Milk', 'Fairlife Milk', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'FairlifeMilk', 'Fairlife Milk', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Core Power', 'Core Power', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'CorePower', 'Core Power', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r"Dunkin'", "Dunkin'", name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Topo Chico', 'Topo Chico', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Tum - E Yummies', 'Tum-E Yummies', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Tum-EYummies', 'Tum-E Yummies', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Storm Zero Sugar', 'Storm Zero Sugar', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'StormZeroSugar', 'Storm Zero Sugar', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Nos Energy', 'NOS Energy', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Nos', 'NOS', name_str)
    name_str = re.sub(r'Full Throttle', 'Full Throttle', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'FullThrottle', 'Full Throttle', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Dasani', 'Dasani', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Hi - C', 'Hi-C', name_str, flags=re.IGNORECASE)
    name_str = re.sub(r'Hi-C', 'Hi-C', name_str, flags=re.IGNORECASE)
    
    # Flavor cleanups
    name_str = re.sub(r'Coca-Cola Cherry Zero\b', 'Coca-Cola Cherry Zero Sugar', name_str)
    name_str = re.sub(r'Coca-Cola Zero Sugar Cherry Float\b', 'Coca-Cola Zero Sugar Cherry Float', name_str)
    name_str = re.sub(r'Coca-Cola Cherry Float\b', 'Coca-Cola Cherry Float', name_str)
    name_str = re.sub(r'Coca-Cola Mexico\b', 'Coca-Cola de Mexico (Glass Bottle)', name_str)
    name_str = re.sub(r'Sprite Mexico\b', 'Sprite de Mexico (Glass Bottle)', name_str)
    name_str = re.sub(r'Fanta Orange Mexico\b', 'Fanta Orange de Mexico (Glass Bottle)', name_str)
    name_str = re.sub(r'Fanta 0range Mexico\b', 'Fanta Orange de Mexico (Glass Bottle)', name_str)
    name_str = re.sub(r'Dr Pepper Strawberries& Cream\b', 'Dr Pepper Strawberries & Cream', name_str)
    name_str = re.sub(r'Dr Pepper Cream Soda\b', 'Dr Pepper & Cream Soda', name_str)
    name_str = re.sub(r'Dr Pepper Blackberry\b', 'Dr Pepper Blackberry', name_str)
    name_str = re.sub(r'Dr Pepper Zero Sugar\b', 'Dr Pepper Zero Sugar', name_str)
    name_str = re.sub(r'Diet Dr Pepper\b', 'Diet Dr Pepper', name_str)
    name_str = re.sub(r'Diet Cherry Coke\b', 'Diet Cherry Coke', name_str)
    name_str = re.sub(r'Sprite Chill\b', 'Sprite Chill', name_str)
    name_str = re.sub(r'Sprite Tropical Mix\b', 'Sprite Tropical Mix', name_str)
    name_str = re.sub(r'Sprite Zero Sugar\b', 'Sprite Zero Sugar', name_str)
    name_str = re.sub(r'Tum-E Yummies Big Berry Blast\b', 'Tum-E Yummies Big Berry Blast', name_str)
    name_str = re.sub(r'Tum-E Yummies Edgy Orange Burst\b', 'Tum-E Yummies Edgy Orange Burst', name_str)
    name_str = re.sub(r'Tum-E Yummies Epic Apple Flip\b', 'Tum-E Yummies Epic Apple Flip', name_str)
    name_str = re.sub(r'Tum-E Yummies Fruit Punch Party\b', 'Tum-E Yummies Fruit Punch Party', name_str)
    name_str = re.sub(r'Gold Peak Extra Sweet Tea\b', 'Gold Peak Extra Sweet Tea', name_str)
    name_str = re.sub(r'Gold Peak Sweetened Black Tea\b', 'Gold Peak Sweetened Black Tea', name_str)
    name_str = re.sub(r'Gold Peak Sweetened Green Tea\b', 'Gold Peak Sweetened Green Tea', name_str)
    name_str = re.sub(r'Gold Peak Unsweetened Black Tea\b', 'Gold Peak Unsweetened Black Tea', name_str)
    name_str = re.sub(r'Gold Peak Zero Sugar Sweet Tea\b', 'Gold Peak Zero Sugar Sweet Tea', name_str)
    name_str = re.sub(r'Powerade Mountain Berry Blast\b', 'Powerade Mountain Berry Blast', name_str)
    name_str = re.sub(r'Powerade Fruit Punch\b', 'Powerade Fruit Punch', name_str)
    name_str = re.sub(r'Powerade Lemon Lime\b', 'Powerade Lemon Lime', name_str)
    name_str = re.sub(r'Powerade Orange\b', 'Powerade Orange', name_str)
    name_str = re.sub(r'Powerade Strawberry Lemonade\b', 'Powerade Strawberry Lemonade', name_str)
    name_str = re.sub(r'Powerade Island Burst\b', 'Powerade Island Burst', name_str)
    name_str = re.sub(r'Powerade Grape\b', 'Powerade Grape', name_str)
    name_str = re.sub(r'Powerade Xtra Sour Green Apple\b', 'Powerade Xtra Sour Green Apple', name_str)
    name_str = re.sub(r'Powerade Xtra Sour Peach Pucker\b', 'Powerade Xtra Sour Peach Pucker', name_str)
    name_str = re.sub(r'Powerade Zero Fruit Punch\b', 'Powerade Zero Fruit Punch', name_str)
    name_str = re.sub(r'Powerade Zero Grape\b', 'Powerade Zero Grape', name_str)
    name_str = re.sub(r'Powerade Zero Mixed Berry\b', 'Powerade Zero Mixed Berry', name_str)
    name_str = re.sub(r'Powerade Zero Orange\b', 'Powerade Zero Orange', name_str)
    name_str = re.sub(r'Powerade Zero Strawberry Smash\b', 'Powerade Zero Strawberry Smash', name_str)
    name_str = re.sub(r'Powerade Power Water Zero Sugar Mountain Berry Blast\b', 'Powerade Power Water Zero Sugar Mountain Berry Blast', name_str)
    name_str = re.sub(r'Powerade Power Water Zero Sugar Strawberry Kiwi\b', 'Powerade Power Water Zero Sugar Strawberry Kiwi', name_str)
    name_str = re.sub(r'Powerade Power Water Zero Sugar Tropical Pineapple\b', 'Powerade Power Water Zero Sugar Tropical Pineapple', name_str)
    name_str = re.sub(r'Powerade Power Water Zero Sugar Watermelon\b', 'Powerade Power Water Zero Sugar Watermelon', name_str)
    name_str = re.sub(r'vitaminwater Zero Sugar Power C\b', 'vitaminwater Zero Sugar Power-C', name_str)
    name_str = re.sub(r'vitaminwater Zero Sugar Squeezed\b', 'vitaminwater Zero Sugar Squeezed (Lemonade)', name_str)
    name_str = re.sub(r'vitaminwater Zero Sugar xxx\b', 'vitaminwater Zero Sugar XXX (Acai-Blueberry-Pomegranate)', name_str)
    name_str = re.sub(r'vitaminwater Zero Sugar Re-Hydrate\b', 'vitaminwater Zero Sugar Re-Hydrate (Strawberry Kiwi)', name_str)
    name_str = re.sub(r'vitaminwater Focus\b', 'vitaminwater Focus (Kiwi-Strawberry)', name_str)
    name_str = re.sub(r'vitaminwater Power C\b', 'vitaminwater Power-C (Dragonfruit)', name_str)
    name_str = re.sub(r'vitaminwater Refresh\b', 'vitaminwater Refresh (Tropical Mango)', name_str)
    name_str = re.sub(r'vitaminwater Essential\b', 'vitaminwater Essential (Orange-Orange)', name_str)
    name_str = re.sub(r'vitaminwater Energy\b', 'vitaminwater Energy (Tropical Citrus)', name_str)
    name_str = re.sub(r'vitaminwater xxx\b', 'vitaminwater XXX (Acai-Blueberry-Pomegranate)', name_str)
    name_str = re.sub(r'vitaminwater Elevate\b', 'vitaminwater Elevate', name_str)
    name_str = re.sub(r'smartwater Alkaline With Antioxidant\b', 'smartwater Alkaline with Antioxidants', name_str)
    name_str = re.sub(r'smartwater Alkaline With Antioxidants\b', 'smartwater Alkaline with Antioxidants', name_str)
    name_str = re.sub(r'Monster Energy Ultra Blue Hawaiian Zero Sugar\b', 'Monster Energy Ultra Blue Hawaiian Zero Sugar', name_str)
    name_str = re.sub(r'Monster Energy Ultra Fantasy Ruby Red Zero Sugar\b', 'Monster Energy Ultra Fantasy Ruby Red Zero Sugar', name_str)
    name_str = re.sub(r'Monster Energy Ultra Punk Punch Zero Sugar\b', 'Monster Energy Ultra Punk Punch Zero Sugar', name_str)
    name_str = re.sub(r'Monster Energy Ultra Red White & Blue Razz Zero Sugar\b', 'Monster Energy Ultra Red White & Blue Razz Zero Sugar', name_str)
    name_str = re.sub(r'Monster Energy Ultra Strawberry Dreams Zero Sugar\b', 'Monster Energy Ultra Strawberry Dreams Zero Sugar', name_str)
    name_str = re.sub(r'Monster Energy Ultra Vice Guava Zero Sugar\b', 'Monster Energy Ultra Vice Guava Zero Sugar', name_str)
    name_str = re.sub(r'Monster Energy Ultra Violet Zero Sugar\b', 'Monster Energy Ultra Violet Zero Sugar', name_str)
    name_str = re.sub(r'Monster Energy Ultra Zero Sugar\b', 'Monster Energy Ultra Zero Sugar (White)', name_str)
    name_str = re.sub(r'Monster Energy Ultra Peachy Keen Zero Sugar\b', 'Monster Energy Ultra Peachy Keen Zero Sugar', name_str)
    name_str = re.sub(r'Monster Energy Ultra Sunrise\b', 'Monster Energy Ultra Sunrise Zero Sugar', name_str)
    name_str = re.sub(r'Monster Energy Ultra Paradise\b', 'Monster Energy Ultra Paradise Zero Sugar', name_str)
    name_str = re.sub(r'Monster Energy Ultra Wild Passion Zero Sugar\b', 'Monster Energy Ultra Wild Passion Zero Sugar', name_str)
    name_str = re.sub(r'Monster Energy Zero Sugar\b', 'Monster Energy Zero Sugar (Green/Black)', name_str)
    name_str = re.sub(r'Monster Energy Juice Mango Loco\b', 'Monster Energy Juice Mango Loco', name_str)
    name_str = re.sub(r'Monster Energy Juice Pacific Punch\b', 'Monster Energy Juice Pacific Punch', name_str)
    name_str = re.sub(r'Monster Energy Juice Pipeline Punch\b', 'Monster Energy Juice Pipeline Punch', name_str)
    name_str = re.sub(r'Monster Energy Juice Rio Punch\b', 'Monster Energy Juice Rio Punch', name_str)
    name_str = re.sub(r'Monster Energy Juice Viking Berry\b', 'Monster Energy Juice Viking Berry', name_str)
    name_str = re.sub(r'Monster Energy Juice Voodoo Grape\b', 'Monster Energy Juice Voodoo Grape', name_str)
    name_str = re.sub(r'Monster Energy Juice Bad Apple\b', 'Monster Energy Juice Bad Apple', name_str)
    name_str = re.sub(r'Monster Energy Juice Strawberry Lemonade\b', 'Monster Energy Juice Aussie Style Lemonade', name_str)
    name_str = re.sub(r'Monster Energy Strawberry Shot Zero Sugar\b', 'Monster Energy Strawberry Shot Zero Sugar', name_str)
    name_str = re.sub(r'Monster Energy Strawberry Shot\b', 'Monster Energy Strawberry Shot', name_str)
    name_str = re.sub(r'Monster Energy Lando Norris Zero Sugar\b', 'Monster Energy Lando Norris Zero Sugar', name_str)
    name_str = re.sub(r'Monster Energy Electric Blue\b', 'Monster Energy Electric Blue', name_str)
    name_str = re.sub(r'Monster Nitro Super Dry\b', 'Monster Nitro Super Dry', name_str)
    name_str = re.sub(r'Monster Import Energy\b', 'Monster Energy Import', name_str)
    name_str = re.sub(r'Mega Monster Energy\b', 'Mega Monster Energy (Resealable Cap)', name_str)
    name_str = re.sub(r'Mega Monster Locarb Energy\b', 'Mega Monster Lo-Carb Energy (Resealable Cap)', name_str)
    name_str = re.sub(r'Monster Locarb Energy\b', 'Monster Energy Lo-Carb (Blue)', name_str)
    name_str = re.sub(r'Monster Reserve Orange Dreamsicle\b', 'Monster Energy Reserve Orange Dreamsicle', name_str)
    name_str = re.sub(r'Reign Total Body Fuel Cherry Limeade\b', 'Reign Total Body Fuel Cherry Limeade', name_str)
    name_str = re.sub(r'Reign Total Body Fuel Reignbow Sherbet\b', 'Reign Total Body Fuel Reignbow Sherbet', name_str)
    name_str = re.sub(r'Reign Total Body Fuel Sour Gummy Worm\b', 'Reign Total Body Fuel Sour Gummy Worm', name_str)
    name_str = re.sub(r'Reign Total Body Fuel Watermelon Sour Gummy\b', 'Reign Total Body Fuel Watermelon Sour Gummy', name_str)
    name_str = re.sub(r'Reign Total Body Fuel White Gummy Bear\b', 'Reign Total Body Fuel White Gummy Bear', name_str)
    name_str = re.sub(r'Reign Total Body Fuel White Haze\b', 'Reign Total Body Fuel White Haze', name_str)
    name_str = re.sub(r'Reign Total Body Fuel Orange Dreamsicle\b', 'Reign Total Body Fuel Orange Dreamsicle', name_str)
    name_str = re.sub(r'Bang Energy American Berry\b', 'Bang Energy American Berry', name_str)
    name_str = re.sub(r'Bang Energy Any Means Orange\b', 'Bang Energy Any Means Orange', name_str)
    name_str = re.sub(r'Bang Energy Black Cherry Vanilla\b', 'Bang Energy Black Cherry Vanilla', name_str)
    name_str = re.sub(r'Bang Energy Blue Razz\b', 'Bang Energy Blue Razz', name_str)
    name_str = re.sub(r'Bang Energy Cotton Candy\b', 'Bang Energy Cotton Candy', name_str)
    name_str = re.sub(r'Bang Energy Lime Pop Drop\b', 'Bang Energy Lime Pop Drop', name_str)
    name_str = re.sub(r'Bang Energy Peach Mango\b', 'Bang Energy Peach Mango', name_str)
    name_str = re.sub(r'Bang Energy Purple Haze\b', 'Bang Energy Purple Haze', name_str)
    name_str = re.sub(r'Bang Energy Star Blast\b', 'Bang Energy Star Blast', name_str)
    name_str = re.sub(r'NOS Energy\b', 'NOS Energy Original', name_str)
    name_str = re.sub(r'NOS Gt Grape\b', 'NOS Energy GT Grape', name_str)
    name_str = re.sub(r'NOS Gran Prix Guava\b', 'NOS Energy Gran Prix Guava', name_str)
    name_str = re.sub(r'NOS Zero\b', 'NOS Energy Zero Sugar', name_str)
    name_str = re.sub(r'Full Throttle Red Apple\b', 'Full Throttle Red Apple', name_str)
    name_str = re.sub(r'Full Throttle\b', 'Full Throttle Original Citrus', name_str)
    name_str = re.sub(r'Storm Zero Sugar Guava Strawberry\b', 'Storm Zero Sugar Guava Strawberry', name_str)
    name_str = re.sub(r'Storm Zero Sugar Harvest Grape\b', 'Storm Zero Sugar Harvest Grape', name_str)
    name_str = re.sub(r'Storm Zero Sugar Tropical\b', 'Storm Zero Sugar Tropical', name_str)
    name_str = re.sub(r'Storm Zero Sugar Valencia Orange\b', 'Storm Zero Sugar Valencia Orange', name_str)
    name_str = re.sub(r'BODYARMOR SuperDrink Strawberry Banana\b', 'BODYARMOR SuperDrink Strawberry Banana', name_str)
    name_str = re.sub(r'BODYARMOR SuperDrink Strawberry Grape\b', 'BODYARMOR SuperDrink Strawberry Grape', name_str)
    name_str = re.sub(r'BODYARMOR SuperDrink Tropical Passionfruit\b', 'BODYARMOR SuperDrink Tropical Passionfruit', name_str)
    name_str = re.sub(r'BODYARMOR SuperDrink Tropical Punch\b', 'BODYARMOR SuperDrink Tropical Punch', name_str)
    name_str = re.sub(r'BODYARMOR SuperDrink Blue Raspberry\b', 'BODYARMOR SuperDrink Blue Raspberry', name_str)
    name_str = re.sub(r'BODYARMOR SuperDrink Fruit Punch\b', 'BODYARMOR SuperDrink Fruit Punch', name_str)
    name_str = re.sub(r'BODYARMOR SuperDrink Orange Mango\b', 'BODYARMOR SuperDrink Orange Mango', name_str)
    name_str = re.sub(r'BODYARMOR LYTE Peach Mango\b', 'BODYARMOR LYTE Peach Mango', name_str)
    name_str = re.sub(r'BODYARMOR Zero Sugar Fruit Punch\b', 'BODYARMOR Zero Sugar Fruit Punch', name_str)
    name_str = re.sub(r'BODYARMOR Zero Sugar Lemon Lime\b', 'BODYARMOR Zero Sugar Lemon Lime', name_str)
    name_str = re.sub(r'BODYARMOR Flash IV Zero Sugar Caffeine Watermelon Punch\b', 'BODYARMOR Flash I.V. Zero Sugar Caffeine Watermelon Punch', name_str)
    name_str = re.sub(r'BODYARMOR Flash IV Zero Sugar Caffeine Pineapple Passionfruit\b', 'BODYARMOR Flash I.V. Zero Sugar Caffeine Pineapple Passionfruit', name_str)
    name_str = re.sub(r'BODYARMOR Flash IV Zero Sugar Lemon Lime\b', 'BODYARMOR Flash I.V. Zero Sugar Lemon Lime', name_str)
    name_str = re.sub(r'BODYARMOR Flash Iv Grape\b', 'BODYARMOR Flash I.V. Grape', name_str)
    name_str = re.sub(r'BODYARMOR Flash Iv Orange\b', 'BODYARMOR Flash I.V. Orange', name_str)
    name_str = re.sub(r'BODYARMOR Flash Iv Strawberry Kiwi\b', 'BODYARMOR Flash I.V. Strawberry Kiwi', name_str)
    name_str = re.sub(r'BODYARMOR Flash Iv Tropical Punch\b', 'BODYARMOR Flash I.V. Tropical Punch', name_str)
    name_str = re.sub(r'BODYARMOR Fit Citrus Grapefruit\b', 'BODYARMOR Fit Citrus Grapefruit', name_str)
    name_str = re.sub(r'BODYARMOR Fit Mixed Berry\b', 'BODYARMOR Fit Mixed Berry', name_str)
    name_str = re.sub(r'BODYARMOR Fit Orange Mango\b', 'BODYARMOR Fit Orange Mango', name_str)
    name_str = re.sub(r'BODYARMOR Fit Tropical Passionfruit\b', 'BODYARMOR Fit Tropical Passionfruit', name_str)
    name_str = re.sub(r'BODYARMOR Fit Watermelon Lime\b', 'BODYARMOR Fit Watermelon Lime', name_str)
    name_str = re.sub(r'BODYARMOR SportWater Alkaline & Electrolytes\b', 'BODYARMOR SportWater Alkaline & Electrolytes', name_str)
    name_str = re.sub(r'Minute Maid Blue Raspberry\b', 'Minute Maid Blue Raspberry', name_str)
    name_str = re.sub(r'Minute Maid Berry Punch\b', 'Minute Maid Berry Punch', name_str)
    name_str = re.sub(r'Minute Maid Fruit Punch\b', 'Minute Maid Fruit Punch', name_str)
    name_str = re.sub(r'Minute Maid Kiwi Strawberry\b', 'Minute Maid Kiwi Strawberry', name_str)
    name_str = re.sub(r'Minute Maid Pineapple Burst\b', 'Minute Maid Pineapple Burst', name_str)
    name_str = re.sub(r'Minute Maid Pink Lemonade\b', 'Minute Maid Pink Lemonade', name_str)
    name_str = re.sub(r'Minute Maid Lemonade\b', 'Minute Maid Lemonade', name_str)
    name_str = re.sub(r'Minute Maid Zero Sugar Lemonade\b', 'Minute Maid Zero Sugar Lemonade', name_str)
    name_str = re.sub(r'Minute Maid Juice-To-Go Apple Juice 100\b', 'Minute Maid Juice-To-Go 100% Apple Juice', name_str)
    name_str = re.sub(r'Minute Maid Juice-To-Go Orange Juice 100\b', 'Minute Maid Juice-To-Go 100% Orange Juice', name_str)
    name_str = re.sub(r'Minute Maid Juice-To-Go Pineapple Orange Juice 100\b', 'Minute Maid Juice-To-Go 100% Pineapple Orange Juice', name_str)
    name_str = re.sub(r'Minute Maid Juice-To-Go Cranberry Grape\b', 'Minute Maid Juice-To-Go Cranberry Grape', name_str)
    name_str = re.sub(r'Minute Maid Juice-To-Go Cranberry Apple Raspberry\b', 'Minute Maid Juice-To-Go Cranberry Apple Raspberry', name_str)
    name_str = re.sub(r'Topo Chico Sabores Blueberry With Hibiscus Extract\b', 'Topo Chico Sabores Blueberry with Hibiscus', name_str)
    name_str = re.sub(r'Topo Chico Sabores Lime With Mint Extract\b', 'Topo Chico Sabores Lime with Mint', name_str)
    name_str = re.sub(r'Topo Chico Sabores Raspberry With Lemon\b', 'Topo Chico Sabores Raspberry with Lemon', name_str)
    name_str = re.sub(r'Topo Chico Sabores Tangerine With Ginger Extract\b', 'Topo Chico Sabores Tangerine with Ginger', name_str)

    # Base name cleanup
    if name_str in ['Coca-Cola', 'Coca-Cola,']:
        name_str = 'Coca-Cola Original Taste'
    elif name_str in ['Diet Coke', 'Diet Coke,']:
        name_str = 'Diet Coke Classic'
    elif name_str in ['Sprite', 'Sprite,']:
        name_str = 'Sprite Lemon-Lime'
    elif name_str in ['Dr Pepper', 'Dr Pepper,']:
        name_str = 'Dr Pepper Original'
    elif name_str in ["Barq's Root Beer", "Barq's Root Beer,"]:
        name_str = "Barq's Root Beer"
    elif name_str in ['Mello Yello', 'Mello Yello,']:
        name_str = 'Mello Yello Citrus'
    elif name_str in ['Dasani', 'Dasani,']:
        name_str = 'Dasani Purified Water'
    elif name_str in ['smartwater', 'smartwater,']:
        name_str = 'smartwater Pure Distilled Water'
    elif name_str in ['Monster Energy', 'Monster Energy,']:
        name_str = 'Monster Energy Original (Green)'
        
    name_str = re.sub(r'[,.\-_:;]+$', '', name_str).strip()
    
    # Categorization and Brand Group
    brand_group = 'Other'
    cat = 'Other Beverages'
    
    nl = name_str.lower()
    
    if 'coca-cola' in nl:
        cat = 'Carbonated Soft Drinks'
        brand_group = 'Coca-Cola'
    elif 'diet coke' in nl or 'diet cherry coke' in nl:
        cat = 'Carbonated Soft Drinks'
        brand_group = 'Diet Coke'
    elif 'sprite' in nl:
        cat = 'Carbonated Soft Drinks'
        brand_group = 'Sprite'
    elif 'dr pepper' in nl:
        cat = 'Carbonated Soft Drinks'
        brand_group = 'Dr Pepper'
    elif 'fanta' in nl:
        cat = 'Carbonated Soft Drinks'
        brand_group = 'Fanta'
    elif 'mello yello' in nl:
        cat = 'Carbonated Soft Drinks'
        brand_group = 'Mello Yello'
    elif "barq's" in nl:
        cat = 'Carbonated Soft Drinks'
        brand_group = "Barq's Root Beer"
    elif "seagram's" in nl:
        cat = 'Carbonated Soft Drinks'
        brand_group = "Seagram's Ginger Ale"
    elif 'java monster' in nl or 'killer brew' in nl:
        cat = 'Energy Drinks'
        brand_group = 'Java Monster Coffee'
    elif 'monster rehab' in nl:
        cat = 'Energy Drinks'
        brand_group = 'Monster Rehab'
    elif 'monster energy ultra' in nl:
        cat = 'Energy Drinks'
        brand_group = 'Monster Energy Ultra'
    elif 'monster energy juice' in nl:
        cat = 'Energy Drinks'
        brand_group = 'Monster Energy Juice'
    elif 'monster' in nl or 'mega monster' in nl:
        cat = 'Energy Drinks'
        brand_group = 'Monster Energy'
    elif 'reign' in nl:
        cat = 'Energy Drinks'
        brand_group = 'Reign Total Body Fuel'
    elif 'bang' in nl:
        cat = 'Energy Drinks'
        brand_group = 'Bang Energy'
    elif 'nos' in nl:
        cat = 'Energy Drinks'
        brand_group = 'NOS Energy'
    elif 'full throttle' in nl:
        cat = 'Energy Drinks'
        brand_group = 'Full Throttle'
    elif 'storm' in nl:
        cat = 'Energy Drinks'
        brand_group = 'Storm Energy'
    elif 'powerade power water' in nl:
        cat = 'Sports & Enhanced Water'
        brand_group = 'Powerade Power Water'
    elif 'powerade' in nl:
        cat = 'Sports & Hydration'
        brand_group = 'Powerade'
    elif 'bodyarmor flash' in nl:
        cat = 'Sports & Hydration'
        brand_group = 'BODYARMOR Flash I.V.'
    elif 'bodyarmor fit' in nl:
        cat = 'Sports & Hydration'
        brand_group = 'BODYARMOR Fit'
    elif 'bodyarmor sportwater' in nl:
        cat = 'Bottled & Enhanced Water'
        brand_group = 'BODYARMOR SportWater'
    elif 'bodyarmor' in nl:
        cat = 'Sports & Hydration'
        brand_group = 'BODYARMOR SuperDrink & Lyte'
    elif 'smartwater' in nl:
        cat = 'Bottled & Enhanced Water'
        brand_group = 'smartwater'
    elif 'vitaminwater' in nl:
        cat = 'Enhanced Water & Wellness'
        brand_group = 'vitaminwater'
    elif 'dasani' in nl:
        cat = 'Bottled & Enhanced Water'
        brand_group = 'Dasani Water'
    elif 'topo chico' in nl:
        cat = 'Sparkling Water & Seltzers'
        brand_group = 'Topo Chico'
    elif 'minute maid' in nl:
        cat = 'Juices & Fruit Drinks'
        brand_group = 'Minute Maid'
    elif 'hi-c' in nl:
        cat = 'Juices & Fruit Drinks'
        brand_group = 'Hi-C'
    elif 'gold peak' in nl:
        cat = 'Ready-to-Drink Teas'
        brand_group = 'Gold Peak Tea'
    elif 'core power' in nl:
        cat = 'Dairy & Protein Drinks'
        brand_group = 'Core Power Protein'
    elif 'fairlife' in nl:
        cat = 'Dairy & Protein Drinks'
        brand_group = 'Fairlife Milk'
    elif "dunkin'" in nl:
        cat = 'Ready-to-Drink Coffee'
        brand_group = "Dunkin' Iced Coffee"
    elif 'tum-e' in nl:
        cat = 'Kids Drinks & Juices'
        brand_group = 'Tum-E Yummies'

    return {
        'sku': sku,
        'upc': upc,
        'category': cat,
        'brand_group': brand_group,
        'full_name': name_str,
        'size': size_str,
        'container_type': ctype,
        'packaging': pack_str,
        'image_path': f'drink_images/sku_{sku}.png'
    }

parsed_all = [parse_entry(sku, entries) for sku, entries in by_sku.items()]

# Sort: Category, Brand Group, Full Name, Size
parsed_all.sort(key=lambda x: (x['category'], x['brand_group'], x['full_name'], x['size']))

with open('drinks_database.json', 'w') as f:
    json.dump(parsed_all, f, indent=2)

print(f"Generated drinks_database.json with {len(parsed_all)} drinks!")
