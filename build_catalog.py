import json
import re

with open('all_detailed_products.json') as f:
    items = json.load(f)

by_sku = {}
for it in items:
    sku = it['sku']
    if not sku:
        continue
    if sku not in by_sku:
        by_sku[sku] = []
    by_sku[sku].append(it)

print(f"Total unique SKUs: {len(by_sku)}")

def build_drink_catalog():
    catalog = []
    
    # Custom Overrides for items that need specific metadata
    manual_overrides = {
        '151817': {'cat': 'Dairy & Protein Drinks', 'brand': 'Core Power Protein', 'name': 'Core Power Protein Chocolate Elite 42g', 'size': '14 oz', 'type': 'Plastic Bottle', 'pack': '12 Loose'},
        '150885': {'cat': 'Energy Drinks', 'brand': 'Monster Rehab', 'name': 'Monster Rehab Tea + Peach', 'size': '15.5 oz', 'type': 'Can', 'pack': '24 Loose'},
        '138036': {'cat': 'Energy Drinks', 'brand': 'Monster Rehab', 'name': 'Monster Rehab Tea + Lemonade', 'size': '15.5 oz', 'type': 'Can', 'pack': '24 Loose'},
        '412029': {'cat': 'Energy Drinks', 'brand': 'Monster Rehab', 'name': 'Monster Rehab Tea + Lemonade', 'size': '18.6 oz', 'type': 'Can', 'pack': '12 Loose'},
        '700015': {'cat': 'Fountain & Supplies', 'brand': 'Cups & Supplies', 'name': 'Cups 12 oz Styrofoam TB', 'size': '12 oz', 'type': 'Cup', 'pack': 'Case'},
        '116965': {'cat': 'Fountain & Supplies', 'brand': 'Cups & Supplies', 'name': 'Cups 16 oz Styrofoam', 'size': '16 oz', 'type': 'Cup', 'pack': 'Case'},
        '144892': {'cat': 'Fountain & Supplies', 'brand': 'Cups & Supplies', 'name': 'Cups 12 oz Paper Trademark', 'size': '12 oz', 'type': 'Cup', 'pack': '2000 Count'},
        '144893': {'cat': 'Fountain & Supplies', 'brand': 'Cups & Supplies', 'name': 'Cups 16 oz Paper Trademark', 'size': '16 oz', 'type': 'Cup', 'pack': '1000 Count'},
        '151208': {'cat': 'Fountain & Supplies', 'brand': 'Bag-in-Box Mixes', 'name': 'Coca-Cola Md Beverage Mix', 'size': '46 oz', 'type': 'Bag-in-Box', 'pack': '1 Box'},
        '151215': {'cat': 'Fountain & Supplies', 'brand': 'Bag-in-Box Mixes', 'name': 'Barqs / Diet Barqs Md Beverage Mix', 'size': '46 oz', 'type': 'Bag-in-Box', 'pack': '1 Box'},
        '151218': {'cat': 'Fountain & Supplies', 'brand': 'Bag-in-Box Mixes', 'name': 'Minute Maid Lemonade / Light Md Beverage Component', 'size': '34 oz', 'type': 'Bag-in-Box', 'pack': '1 Box'},
        '412321': {'cat': 'Fountain & Supplies', 'brand': 'Bag-in-Box Mixes', 'name': 'Seagrams Ginger Ale / Zero Sugar Ginger Ale Md Beverage Mix', 'size': '36 oz', 'type': 'Bag-in-Box', 'pack': '1 Box'},
        '412322': {'cat': 'Fountain & Supplies', 'brand': 'Bag-in-Box Mixes', 'name': 'Mello Yello / Mello Yello Zero Md Beverage Mix', 'size': '36 oz', 'type': 'Bag-in-Box', 'pack': '1 Box'},
        '150932': {'cat': 'Fountain & Supplies', 'brand': 'Bag-in-Box Mixes', 'name': 'Powerade Md Beverage Component', 'size': '23 oz', 'type': 'Bag-in-Box', 'pack': '1 Box'},
        '152098': {'cat': 'Fountain & Supplies', 'brand': 'Bag-in-Box Mixes', 'name': 'Glaceau Vitaminwater Md Beverage Component', 'size': '11.5 oz', 'type': 'Bag-in-Box', 'pack': '1 Box'},
        '104235': {'cat': 'Fountain & Supplies', 'brand': 'Bag-in-Box Syrups', 'name': "Barq's Root Beer Bag-in-Box Syrup", 'size': '2.5 Gal', 'type': 'Bag-in-Box', 'pack': '1 Box'},
        '104148': {'cat': 'Fountain & Supplies', 'brand': 'Bag-in-Box Syrups', 'name': 'Hi-C Fruit Punch Bag-in-Box Syrup', 'size': '2.5 Gal', 'type': 'Bag-in-Box', 'pack': '1 Box'},
        '103895': {'cat': 'Fountain & Supplies', 'brand': 'Bag-in-Box Syrups', 'name': 'Hi-C Pink Lemonade Bag-in-Box Syrup', 'size': '2.5 Gal', 'type': 'Bag-in-Box', 'pack': '1 Box'},
        '109147': {'cat': 'Fountain & Supplies', 'brand': 'Bag-in-Box Syrups', 'name': 'Minute Maid Lemonade Bag-in-Box Syrup', 'size': '2.5 Gal', 'type': 'Bag-in-Box', 'pack': '1 Box'},
        '104239': {'cat': 'Fountain & Supplies', 'brand': 'Bag-in-Box Syrups', 'name': 'Powerade Mountain Blast Bag-in-Box Syrup', 'size': '2.5 Gal', 'type': 'Bag-in-Box', 'pack': '1 Box'},
        '132766': {'cat': 'Fountain & Supplies', 'brand': 'Bag-in-Box Syrups', 'name': 'Gold Peak Premium Unsweetened Tea Bag-in-Box Syrup', 'size': '2.5 Gal', 'type': 'Bag-in-Box', 'pack': '1 Box'},
        '139200': {'cat': 'Fountain & Supplies', 'brand': 'Bag-in-Box Syrups', 'name': 'Gold Peak Southern Style Tea Bag-in-Box Syrup', 'size': '5 Gal', 'type': 'Bag-in-Box', 'pack': '1 Box'},
        '156188': {'cat': 'Dairy & Protein Drinks', 'brand': 'Core Power Protein', 'name': 'Core Power Protein Strawberry Banana 26g', 'size': '14 oz', 'type': 'Plastic Bottle', 'pack': '12 Loose'},
        '157128': {'cat': 'Dairy & Protein Drinks', 'brand': 'Core Power Protein', 'name': 'Core Power Protein Strawberry Elite 42g', 'size': '14 oz', 'type': 'Plastic Bottle', 'pack': '12 Loose'},
        '156182': {'cat': 'Dairy & Protein Drinks', 'brand': 'Core Power Protein', 'name': 'Core Power Protein Vanilla 26g', 'size': '14 oz', 'type': 'Plastic Bottle', 'pack': '12 Loose'},
        '151818': {'cat': 'Dairy & Protein Drinks', 'brand': 'Core Power Protein', 'name': 'Core Power Protein Vanilla Elite 42g', 'size': '14 oz', 'type': 'Plastic Bottle', 'pack': '12 Loose'},
        '156184': {'cat': 'Dairy & Protein Drinks', 'brand': 'Core Power Protein', 'name': 'Core Power Protein Chocolate 26g', 'size': '14 oz', 'type': 'Plastic Bottle', 'pack': '12 Loose'},
        '410721': {'cat': 'Dairy & Protein Drinks', 'brand': 'Fairlife Milk', 'name': 'Fairlife 2% Chocolate Ultra-Filtered Milk', 'size': '14 oz', 'type': 'Plastic Bottle', 'pack': '12 Loose'},
        '411523': {'cat': 'Dairy & Protein Drinks', 'brand': 'Fairlife Milk', 'name': 'Fairlife 2% Reduced Fat Ultra-Filtered Milk', 'size': '14 oz', 'type': 'Plastic Bottle', 'pack': '12 Loose'},
        '411524': {'cat': 'Dairy & Protein Drinks', 'brand': 'Fairlife Milk', 'name': 'Fairlife 2% Strawberry Ultra-Filtered Milk', 'size': '14 oz', 'type': 'Plastic Bottle', 'pack': '12 Loose'},
        '412451': {'cat': 'Ready-to-Drink Coffee', 'brand': "Dunkin' Iced Coffee", 'name': "Dunkin' Caramel Iced Coffee", 'size': '13.7 oz', 'type': 'Plastic Bottle', 'pack': '12 Loose'},
        '152921': {'cat': 'Ready-to-Drink Coffee', 'brand': "Dunkin' Iced Coffee", 'name': "Dunkin' French Vanilla Iced Coffee", 'size': '13.7 oz', 'type': 'Plastic Bottle', 'pack': '12 Loose'},
        '152922': {'cat': 'Ready-to-Drink Coffee', 'brand': "Dunkin' Iced Coffee", 'name': "Dunkin' Mocha Iced Coffee", 'size': '13.7 oz', 'type': 'Plastic Bottle', 'pack': '12 Loose'},
        '152923': {'cat': 'Ready-to-Drink Coffee', 'brand': "Dunkin' Iced Coffee", 'name': "Dunkin' Original Iced Coffee", 'size': '13.7 oz', 'type': 'Plastic Bottle', 'pack': '12 Loose'},
        '413935': {'cat': 'Ready-to-Drink Coffee', 'brand': "Dunkin' Iced Coffee", 'name': "Dunkin' Double Espresso - Original", 'size': '15 oz', 'type': 'Can', 'pack': '12 Loose'},
        '413616': {'cat': 'Ready-to-Drink Coffee', 'brand': "Dunkin' Iced Coffee", 'name': "Dunkin' Double Espresso - Cafe Mocha", 'size': '15 oz', 'type': 'Can', 'pack': '12 Loose'},
        '412030': {'cat': 'Energy Drinks', 'brand': 'Java Monster Coffee', 'name': 'Java Monster Cafe Latte', 'size': '15 oz', 'type': 'Can', 'pack': '12 Loose'},
        '134923': {'cat': 'Energy Drinks', 'brand': 'Java Monster Coffee', 'name': 'Java Monster Irish Blend', 'size': '15 oz', 'type': 'Can', 'pack': '12 Loose'},
        '134929': {'cat': 'Energy Drinks', 'brand': 'Java Monster Coffee', 'name': 'Java Monster Loca Moca', 'size': '15 oz', 'type': 'Can', 'pack': '12 Loose'},
        '134926': {'cat': 'Energy Drinks', 'brand': 'Java Monster Coffee', 'name': 'Java Monster Mean Bean', 'size': '15 oz', 'type': 'Can', 'pack': '12 Loose'},
        '151811': {'cat': 'Energy Drinks', 'brand': 'Java Monster Coffee', 'name': 'Java Monster Salted Caramel', 'size': '15 oz', 'type': 'Can', 'pack': '12 Loose'},
        '413306': {'cat': 'Energy Drinks', 'brand': 'Java Monster Coffee', 'name': 'Monster Killer Brew Loca Moca', 'size': '15 oz', 'type': 'Can', 'pack': '12 Loose'},
        '413346': {'cat': 'Energy Drinks', 'brand': 'Java Monster Coffee', 'name': 'Monster Killer Brew Mean Bean', 'size': '15 oz', 'type': 'Can', 'pack': '12 Loose'},
        '412588': {'cat': 'Energy Drinks', 'brand': 'Monster Rehab', 'name': 'Monster Rehab Green Tea + Energy', 'size': '15.5 oz', 'type': 'Can', 'pack': '24 Loose'},
        '412182': {'cat': 'Energy Drinks', 'brand': 'Monster Rehab', 'name': 'Monster Rehab Wild Berry Tea', 'size': '15.5 oz', 'type': 'Can', 'pack': '24 Loose'},
    }
    
    for sku, entries in by_sku.items():
        best = max(entries, key=lambda x: (x['crop_h'], len(' '.join(x['title_lines']))))
        upc = ''
        for e in entries:
            if e['upc'] and len(e['upc']) >= 8:
                upc = e['upc']
                break
                
        if sku in manual_overrides:
            ov = manual_overrides[sku]
            catalog.append({
                'id': f"drink-{sku}",
                'sku': sku,
                'upc': upc,
                'category': ov['cat'],
                'brand_group': ov['brand'],
                'full_name': ov['name'],
                'size': ov['size'],
                'container_type': ov['type'],
                'packaging': ov['pack'],
                'image_path': f"drink_images/sku_{sku}.png"
            })
            continue
            
        raw_text = ' '.join(best['title_lines'])
        raw_text = re.sub(r'^(Add\s*to\s*Cart|AddtoCart|Add toCart|\+|\-|\×|\中|\十|\–|\*)\s*', '', raw_text, flags=re.IGNORECASE)
        raw_text = re.sub(r'\s*(Add\s*to\s*Cart|AddtoCart|Add toCart|\+|\-|\×|\中|\十|\–|\*)$', '', raw_text, flags=re.IGNORECASE)
        raw_text = re.sub(r'^\s*[,.\-_:;]+\s*', '', raw_text)
        raw_text = re.sub(r'\s*[,.\-_:;]+$', '', raw_text)

        # Match size
        size_m = re.search(r'(\d+(?:\.\d+)?)\s*(oz|ltr|Itr|liter|L|gal|ml)\b', raw_text, re.IGNORECASE)
        if not size_m:
            size_m = re.search(r'(\d+(?:\.\d+)?)\s*(oz|ltr|Itr|liter|L|gal|ml)', raw_text, re.IGNORECASE)
            
        size = ''
        name_raw = raw_text
        if size_m:
            val = size_m.group(1)
            unit = size_m.group(2).lower()
            if unit in ['itr', 'ltr', 'liter', 'l']:
                u_str = 'Liter'
            elif unit == 'oz':
                u_str = 'oz'
            elif unit == 'gal':
                u_str = 'Gal'
            elif unit == 'ml':
                u_str = 'mL'
            else:
                u_str = unit
            size = f"{val} {u_str}"
            name_raw = raw_text[:size_m.start()].strip()
            
        # Match pack
        pack = ''
        if re.search(r'12\s*pk\s*[,，]?\s*2\s*ct', raw_text, re.IGNORECASE):
            pack = '12 Pack (2 CT)'
        elif re.search(r'15\s*pk\s*[,，]?\s*2\s*ct', raw_text, re.IGNORECASE):
            pack = '15 Pack (2 CT)'
        elif re.search(r'6\s*pk\s*[,，]?\s*4\s*ct', raw_text, re.IGNORECASE):
            pack = '6 Pack (4 CT)'
        elif re.search(r'4\s*pk\s*[,，]?\s*6\s*ct', raw_text, re.IGNORECASE):
            pack = '4 Pack (6 CT)'
        elif re.search(r'8\s*pk', raw_text, re.IGNORECASE):
            pack = '8 Pack'
        elif re.search(r'24\s*pk', raw_text, re.IGNORECASE):
            pack = '24 Pack Case'
        elif re.search(r'24\s*(?:loose|lo0se|l\b|lo\b)', raw_text, re.IGNORECASE):
            pack = '24 Loose'
        elif re.search(r'12\s*(?:loose|lo0se|l\b|lo\b)', raw_text, re.IGNORECASE):
            pack = '12 Loose'
        elif re.search(r'15\s*(?:loose|lo0se|l\b|lo\b)', raw_text, re.IGNORECASE):
            pack = '15 Loose'
        elif re.search(r'8\s*(?:loose|lo0se|l\b|lo\b)', raw_text, re.IGNORECASE):
            pack = '8 Loose'
            
        # Clean name
        name = name_raw
        name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
        name = re.sub(r'([A-Za-z])(\d)', r'\1 \2', name)
        name = re.sub(r'(\d)([A-Za-z])', r'\1 \2', name)
        name = re.sub(r'\s+', ' ', name).strip()
        name = re.sub(r'[,.\-_:;]+$', '', name).strip()
        
        # Container type
        ctype = 'Plastic Bottle'
        if 'can' in raw_text.lower():
            ctype = 'Can'
        elif 'bag-in-box' in raw_text.lower():
            ctype = 'Bag-in-Box'
        elif 'mexico' in raw_text.lower() or '355' in raw_text or ('8 oz' in size and 'bottle' in raw_text.lower()):
            ctype = 'Glass Bottle'
        elif 'cup' in raw_text.lower():
            ctype = 'Cup'
            
        # Brand standard replacements
        replacements = [
            (r'Coca - Cola', 'Coca-Cola'),
            (r'Coca Cola', 'Coca-Cola'),
            (r'DrPepper', 'Dr Pepper'),
            (r'Dr Pepper', 'Dr Pepper'),
            (r'DietDrPepper', 'Diet Dr Pepper'),
            (r'Diet DrPepper', 'Diet Dr Pepper'),
            (r'Diet Coke', 'Diet Coke'),
            (r'DietCherryCoke', 'Diet Cherry Coke'),
            (r'Diet Cherry Coke', 'Diet Cherry Coke'),
            (r'SpriteChill', 'Sprite Chill'),
            (r'Sprite Tropical Mix', 'Sprite Tropical Mix'),
            (r'SpriteZeroSugar', 'Sprite Zero Sugar'),
            (r'Barqs', "Barq's"),
            (r'MelloYello', 'Mello Yello'),
            (r'Seagrams', "Seagram's"),
            (r'Glaceau Smartwater', 'smartwater'),
            (r'Glaceau Vitaminwater', 'vitaminwater'),
            (r'Glaceausmartwater', 'smartwater'),
            (r'Glaceauvitaminwater', 'vitaminwater'),
            (r'MinuteMaid', 'Minute Maid'),
            (r'Powerade', 'Powerade'),
            (r'Bodyarmor', 'BODYARMOR'),
            (r'Reign Total Body Fuel', 'Reign Total Body Fuel'),
            (r'ReignTotalBodyFuel', 'Reign Total Body Fuel'),
            (r'Bang Energy', 'Bang Energy'),
            (r'BangEnergy', 'Bang Energy'),
            (r'Monster Energy', 'Monster Energy'),
            (r'MonsterEnergy', 'Monster Energy'),
            (r'Gold Peak', 'Gold Peak'),
            (r'GoldPeak', 'Gold Peak'),
            (r'Fairlife Milk', 'Fairlife Milk'),
            (r'FairlifeMilk', 'Fairlife Milk'),
            (r'Core Power', 'Core Power'),
            (r'CorePower', 'Core Power'),
            (r"Dunkin'", "Dunkin'"),
            (r'Topo Chico', 'Topo Chico'),
            (r'Tum - E Yummies', 'Tum-E Yummies'),
            (r'Tum-EYummies', 'Tum-E Yummies'),
            (r'Storm Zero Sugar', 'Storm Zero Sugar'),
            (r'StormZeroSugar', 'Storm Zero Sugar'),
            (r'Nos Energy', 'NOS Energy'),
            (r'Nos', 'NOS'),
            (r'Full Throttle', 'Full Throttle'),
            (r'FullThrottle', 'Full Throttle'),
            (r'Dasani', 'Dasani'),
            (r'Hi - C', 'Hi-C'),
            (r'Hi-C', 'Hi-C'),
            (r'Coca-Cola Cherry Zero\b', 'Coca-Cola Cherry Zero Sugar'),
            (r'Coca-Cola Zero Sugar Cherry Float\b', 'Coca-Cola Zero Sugar Cherry Float'),
            (r'Coca-Cola Cherry Float\b', 'Coca-Cola Cherry Float'),
            (r'Coca-Cola Mexico\b', 'Coca-Cola de Mexico (Glass Bottle)'),
            (r'Sprite Mexico\b', 'Sprite de Mexico (Glass Bottle)'),
            (r'Fanta Orange Mexico\b', 'Fanta Orange de Mexico (Glass Bottle)'),
            (r'Fanta 0range Mexico\b', 'Fanta Orange de Mexico (Glass Bottle)'),
            (r'Dr Pepper Strawberries& Cream\b', 'Dr Pepper Strawberries & Cream'),
            (r'Dr Pepper Cream Soda\b', 'Dr Pepper & Cream Soda'),
            (r'Dr Pepper Blackberry\b', 'Dr Pepper Blackberry'),
            (r'Dr Pepper Zero Sugar\b', 'Dr Pepper Zero Sugar'),
            (r'Diet Dr Pepper\b', 'Diet Dr Pepper'),
            (r'Diet Cherry Coke\b', 'Diet Cherry Coke'),
            (r'Sprite Chill\b', 'Sprite Chill'),
            (r'Sprite Tropical Mix\b', 'Sprite Tropical Mix'),
            (r'Sprite Zero Sugar\b', 'Sprite Zero Sugar'),
            (r'Tum-E Yummies Big Berry Blast\b', 'Tum-E Yummies Big Berry Blast'),
            (r'Tum-E Yummies Edgy Orange Burst\b', 'Tum-E Yummies Edgy Orange Burst'),
            (r'Tum-E Yummies Epic Apple Flip\b', 'Tum-E Yummies Epic Apple Flip'),
            (r'Tum-E Yummies Fruit Punch Party\b', 'Tum-E Yummies Fruit Punch Party'),
            (r'Gold Peak Extra Sweet Tea\b', 'Gold Peak Extra Sweet Tea'),
            (r'Gold Peak Sweetened Black Tea\b', 'Gold Peak Sweetened Black Tea'),
            (r'Gold Peak Sweetened Green Tea\b', 'Gold Peak Sweetened Green Tea'),
            (r'Gold Peak Unsweetened Black Tea\b', 'Gold Peak Unsweetened Black Tea'),
            (r'Gold Peak Zero Sugar Sweet Tea\b', 'Gold Peak Zero Sugar Sweet Tea'),
            (r'Powerade Mountain Berry Blast\b', 'Powerade Mountain Berry Blast'),
            (r'Powerade Fruit Punch\b', 'Powerade Fruit Punch'),
            (r'Powerade Lemon Lime\b', 'Powerade Lemon Lime'),
            (r'Powerade Orange\b', 'Powerade Orange'),
            (r'Powerade Strawberry Lemonade\b', 'Powerade Strawberry Lemonade'),
            (r'Powerade Island Burst\b', 'Powerade Island Burst'),
            (r'Powerade Grape\b', 'Powerade Grape'),
            (r'Powerade Xtra Sour Green Apple\b', 'Powerade Xtra Sour Green Apple'),
            (r'Powerade Xtra Sour Peach Pucker\b', 'Powerade Xtra Sour Peach Pucker'),
            (r'Powerade Zero Fruit Punch\b', 'Powerade Zero Fruit Punch'),
            (r'Powerade Zero Grape\b', 'Powerade Zero Grape'),
            (r'Powerade Zero Mixed Berry\b', 'Powerade Zero Mixed Berry'),
            (r'Powerade Zero Orange\b', 'Powerade Zero Orange'),
            (r'Powerade Zero Strawberry Smash\b', 'Powerade Zero Strawberry Smash'),
            (r'Powerade Power Water Zero Sugar Mountain Berry Blast\b', 'Powerade Power Water Zero Sugar Mountain Berry Blast'),
            (r'Powerade Power Water Zero Sugar Strawberry Kiwi\b', 'Powerade Power Water Zero Sugar Strawberry Kiwi'),
            (r'Powerade Power Water Zero Sugar Tropical Pineapple\b', 'Powerade Power Water Zero Sugar Tropical Pineapple'),
            (r'Powerade Power Water Zero Sugar Watermelon\b', 'Powerade Power Water Zero Sugar Watermelon'),
            (r'vitaminwater Zero Sugar Power C\b', 'vitaminwater Zero Sugar Power-C'),
            (r'vitaminwater Zero Sugar Squeezed\b', 'vitaminwater Zero Sugar Squeezed (Lemonade)'),
            (r'vitaminwater Zero Sugar xxx\b', 'vitaminwater Zero Sugar XXX (Acai-Blueberry-Pomegranate)'),
            (r'vitaminwater Zero Sugar Re-Hydrate\b', 'vitaminwater Zero Sugar Re-Hydrate (Strawberry Kiwi)'),
            (r'vitaminwater Focus\b', 'vitaminwater Focus (Kiwi-Strawberry)'),
            (r'vitaminwater Power C\b', 'vitaminwater Power-C (Dragonfruit)'),
            (r'vitaminwater Refresh\b', 'vitaminwater Refresh (Tropical Mango)'),
            (r'vitaminwater Essential\b', 'vitaminwater Essential (Orange-Orange)'),
            (r'vitaminwater Energy\b', 'vitaminwater Energy (Tropical Citrus)'),
            (r'vitaminwater xxx\b', 'vitaminwater XXX (Acai-Blueberry-Pomegranate)'),
            (r'vitaminwater Elevate\b', 'vitaminwater Elevate'),
            (r'smartwater Alkaline With Antioxidant\b', 'smartwater Alkaline with Antioxidants'),
            (r'smartwater Alkaline With Antioxidants\b', 'smartwater Alkaline with Antioxidants'),
            (r'Monster Energy Ultra Blue Hawaiian Zero Sugar\b', 'Monster Energy Ultra Blue Hawaiian Zero Sugar'),
            (r'Monster Energy Ultra Fantasy Ruby Red Zero Sugar\b', 'Monster Energy Ultra Fantasy Ruby Red Zero Sugar'),
            (r'Monster Energy Ultra Punk Punch Zero Sugar\b', 'Monster Energy Ultra Punk Punch Zero Sugar'),
            (r'Monster Energy Ultra Red White & Blue Razz Zero Sugar\b', 'Monster Energy Ultra Red White & Blue Razz Zero Sugar'),
            (r'Monster Energy Ultra Strawberry Dreams Zero Sugar\b', 'Monster Energy Ultra Strawberry Dreams Zero Sugar'),
            (r'Monster Energy Ultra Vice Guava Zero Sugar\b', 'Monster Energy Ultra Vice Guava Zero Sugar'),
            (r'Monster Energy Ultra Violet Zero Sugar\b', 'Monster Energy Ultra Violet Zero Sugar'),
            (r'Monster Energy Ultra Zero Sugar\b', 'Monster Energy Ultra Zero Sugar (White)'),
            (r'Monster Energy Ultra Peachy Keen Zero Sugar\b', 'Monster Energy Ultra Peachy Keen Zero Sugar'),
            (r'Monster Energy Ultra Sunrise\b', 'Monster Energy Ultra Sunrise Zero Sugar'),
            (r'Monster Energy Ultra Paradise\b', 'Monster Energy Ultra Paradise Zero Sugar'),
            (r'Monster Energy Ultra Wild Passion Zero Sugar\b', 'Monster Energy Ultra Wild Passion Zero Sugar'),
            (r'Monster Energy Zero Sugar\b', 'Monster Energy Zero Sugar (Green/Black)'),
            (r'Monster Energy Juice Mango Loco\b', 'Monster Energy Juice Mango Loco'),
            (r'Monster Energy Juice Pacific Punch\b', 'Monster Energy Juice Pacific Punch'),
            (r'Monster Energy Juice Pipeline Punch\b', 'Monster Energy Juice Pipeline Punch'),
            (r'Monster Energy Juice Rio Punch\b', 'Monster Energy Juice Rio Punch'),
            (r'Monster Energy Juice Viking Berry\b', 'Monster Energy Juice Viking Berry'),
            (r'Monster Energy Juice Voodoo Grape\b', 'Monster Energy Juice Voodoo Grape'),
            (r'Monster Energy Juice Bad Apple\b', 'Monster Energy Juice Bad Apple'),
            (r'Monster Energy Juice Strawberry Lemonade\b', 'Monster Energy Juice Aussie Style Lemonade'),
            (r'Monster Energy Strawberry Shot Zero Sugar\b', 'Monster Energy Strawberry Shot Zero Sugar'),
            (r'Monster Energy Strawberry Shot\b', 'Monster Energy Strawberry Shot'),
            (r'Monster Energy Lando Norris Zero Sugar\b', 'Monster Energy Lando Norris Zero Sugar'),
            (r'Monster Energy Electric Blue\b', 'Monster Energy Electric Blue'),
            (r'Monster Nitro Super Dry\b', 'Monster Nitro Super Dry'),
            (r'Monster Import Energy\b', 'Monster Energy Import'),
            (r'Mega Monster Energy\b', 'Mega Monster Energy (Resealable Cap)'),
            (r'Mega Monster Locarb Energy\b', 'Mega Monster Lo-Carb Energy (Resealable Cap)'),
            (r'Monster Locarb Energy\b', 'Monster Energy Lo-Carb (Blue)'),
            (r'Monster Reserve Orange Dreamsicle\b', 'Monster Energy Reserve Orange Dreamsicle'),
            (r'Reign Total Body Fuel Cherry Limeade\b', 'Reign Total Body Fuel Cherry Limeade'),
            (r'Reign Total Body Fuel Reignbow Sherbet\b', 'Reign Total Body Fuel Reignbow Sherbet'),
            (r'Reign Total Body Fuel Sour Gummy Worm\b', 'Reign Total Body Fuel Sour Gummy Worm'),
            (r'Reign Total Body Fuel Watermelon Sour Gummy\b', 'Reign Total Body Fuel Watermelon Sour Gummy'),
            (r'Reign Total Body Fuel White Gummy Bear\b', 'Reign Total Body Fuel White Gummy Bear'),
            (r'Reign Total Body Fuel White Haze\b', 'Reign Total Body Fuel White Haze'),
            (r'Reign Total Body Fuel Orange Dreamsicle\b', 'Reign Total Body Fuel Orange Dreamsicle'),
            (r'Bang Energy American Berry\b', 'Bang Energy American Berry'),
            (r'Bang Energy Any Means Orange\b', 'Bang Energy Any Means Orange'),
            (r'Bang Energy Black Cherry Vanilla\b', 'Bang Energy Black Cherry Vanilla'),
            (r'Bang Energy Blue Razz\b', 'Bang Energy Blue Razz'),
            (r'Bang Energy Cotton Candy\b', 'Bang Energy Cotton Candy'),
            (r'Bang Energy Lime Pop Drop\b', 'Bang Energy Lime Pop Drop'),
            (r'Bang Energy Peach Mango\b', 'Bang Energy Peach Mango'),
            (r'Bang Energy Purple Haze\b', 'Bang Energy Purple Haze'),
            (r'Bang Energy Star Blast\b', 'Bang Energy Star Blast'),
            (r'NOS Energy\b', 'NOS Energy Original'),
            (r'NOS Gt Grape\b', 'NOS Energy GT Grape'),
            (r'NOS Gran Prix Guava\b', 'NOS Energy Gran Prix Guava'),
            (r'NOS Zero\b', 'NOS Energy Zero Sugar'),
            (r'Full Throttle Red Apple\b', 'Full Throttle Red Apple'),
            (r'Full Throttle\b', 'Full Throttle Original Citrus'),
            (r'Storm Zero Sugar Guava Strawberry\b', 'Storm Zero Sugar Guava Strawberry'),
            (r'Storm Zero Sugar Harvest Grape\b', 'Storm Zero Sugar Harvest Grape'),
            (r'Storm Zero Sugar Tropical\b', 'Storm Zero Sugar Tropical'),
            (r'Storm Zero Sugar Valencia Orange\b', 'Storm Zero Sugar Valencia Orange'),
            (r'BODYARMOR SuperDrink Strawberry Banana\b', 'BODYARMOR SuperDrink Strawberry Banana'),
            (r'BODYARMOR SuperDrink Strawberry Grape\b', 'BODYARMOR SuperDrink Strawberry Grape'),
            (r'BODYARMOR SuperDrink Tropical Passionfruit\b', 'BODYARMOR SuperDrink Tropical Passionfruit'),
            (r'BODYARMOR SuperDrink Tropical Punch\b', 'BODYARMOR SuperDrink Tropical Punch'),
            (r'BODYARMOR SuperDrink Blue Raspberry\b', 'BODYARMOR SuperDrink Blue Raspberry'),
            (r'BODYARMOR SuperDrink Fruit Punch\b', 'BODYARMOR SuperDrink Fruit Punch'),
            (r'BODYARMOR SuperDrink Orange Mango\b', 'BODYARMOR SuperDrink Orange Mango'),
            (r'BODYARMOR LYTE Peach Mango\b', 'BODYARMOR LYTE Peach Mango'),
            (r'BODYARMOR Zero Sugar Fruit Punch\b', 'BODYARMOR Zero Sugar Fruit Punch'),
            (r'BODYARMOR Zero Sugar Lemon Lime\b', 'BODYARMOR Zero Sugar Lemon Lime'),
            (r'BODYARMOR Flash IV Zero Sugar Caffeine Watermelon Punch\b', 'BODYARMOR Flash I.V. Zero Sugar Caffeine Watermelon Punch'),
            (r'BODYARMOR Flash IV Zero Sugar Caffeine Pineapple Passionfruit\b', 'BODYARMOR Flash I.V. Zero Sugar Caffeine Pineapple Passionfruit'),
            (r'BODYARMOR Flash IV Zero Sugar Lemon Lime\b', 'BODYARMOR Flash I.V. Zero Sugar Lemon Lime'),
            (r'BODYARMOR Flash Iv Grape\b', 'BODYARMOR Flash I.V. Grape'),
            (r'BODYARMOR Flash Iv Orange\b', 'BODYARMOR Flash I.V. Orange'),
            (r'BODYARMOR Flash Iv Strawberry Kiwi\b', 'BODYARMOR Flash I.V. Strawberry Kiwi'),
            (r'BODYARMOR Flash Iv Tropical Punch\b', 'BODYARMOR Flash I.V. Tropical Punch'),
            (r'BODYARMOR Fit Citrus Grapefruit\b', 'BODYARMOR Fit Citrus Grapefruit'),
            (r'BODYARMOR Fit Mixed Berry\b', 'BODYARMOR Fit Mixed Berry'),
            (r'BODYARMOR Fit Orange Mango\b', 'BODYARMOR Fit Orange Mango'),
            (r'BODYARMOR Fit Tropical Passionfruit\b', 'BODYARMOR Fit Tropical Passionfruit'),
            (r'BODYARMOR Fit Watermelon Lime\b', 'BODYARMOR Fit Watermelon Lime'),
            (r'BODYARMOR SportWater Alkaline & Electrolytes\b', 'BODYARMOR SportWater Alkaline & Electrolytes'),
            (r'Minute Maid Blue Raspberry\b', 'Minute Maid Blue Raspberry'),
            (r'Minute Maid Berry Punch\b', 'Minute Maid Berry Punch'),
            (r'Minute Maid Fruit Punch\b', 'Minute Maid Fruit Punch'),
            (r'Minute Maid Kiwi Strawberry\b', 'Minute Maid Kiwi Strawberry'),
            (r'Minute Maid Pineapple Burst\b', 'Minute Maid Pineapple Burst'),
            (r'Minute Maid Pink Lemonade\b', 'Minute Maid Pink Lemonade'),
            (r'Minute Maid Lemonade\b', 'Minute Maid Lemonade'),
            (r'Minute Maid Zero Sugar Lemonade\b', 'Minute Maid Zero Sugar Lemonade'),
            (r'Minute Maid Juice-To-Go Apple Juice 100\b', 'Minute Maid Juice-To-Go 100% Apple Juice'),
            (r'Minute Maid Juice-To-Go Orange Juice 100\b', 'Minute Maid Juice-To-Go 100% Orange Juice'),
            (r'Minute Maid Juice-To-Go Pineapple Orange Juice 100\b', 'Minute Maid Juice-To-Go 100% Pineapple Orange Juice'),
            (r'Minute Maid Juice-To-Go Cranberry Grape\b', 'Minute Maid Juice-To-Go Cranberry Grape'),
            (r'Minute Maid Juice-To-Go Cranberry Apple Raspberry\b', 'Minute Maid Juice-To-Go Cranberry Apple Raspberry'),
            (r'Topo Chico Sabores Blueberry With Hibiscus Extract\b', 'Topo Chico Sabores Blueberry with Hibiscus'),
            (r'Topo Chico Sabores Lime With Mint Extract\b', 'Topo Chico Sabores Lime with Mint'),
            (r'Topo Chico Sabores Raspberry With Lemon\b', 'Topo Chico Sabores Raspberry with Lemon'),
            (r'Topo Chico Sabores Tangerine With Ginger Extract\b', 'Topo Chico Sabores Tangerine with Ginger'),
        ]
        
        for pat, rep in replacements:
            name = re.sub(pat, rep, name, flags=re.IGNORECASE)
            
        if name in ['Coca-Cola', 'Coca-Cola,']:
            name = 'Coca-Cola Original Taste'
        elif name in ['Diet Coke', 'Diet Coke,']:
            name = 'Diet Coke Classic'
        elif name in ['Sprite', 'Sprite,']:
            name = 'Sprite Lemon-Lime'
        elif name in ['Dr Pepper', 'Dr Pepper,']:
            name = 'Dr Pepper Original'
        elif name in ["Barq's Root Beer", "Barq's Root Beer,"]:
            name = "Barq's Root Beer"
        elif name in ['Mello Yello', 'Mello Yello,']:
            name = 'Mello Yello Citrus'
        elif name in ['Dasani', 'Dasani,']:
            name = 'Dasani Purified Water'
        elif name in ['smartwater', 'smartwater,']:
            name = 'smartwater Pure Distilled Water'
        elif name in ['Monster Energy', 'Monster Energy,']:
            name = 'Monster Energy Original (Green)'
            
        name = re.sub(r'[,.\-_:;]+$', '', name).strip()
        
        # Categorization & Brand
        nl = name.lower()
        cat = 'Other Beverages'
        brand = 'Other'
        
        if 'coca-cola' in nl:
            cat = 'Carbonated Soft Drinks'
            brand = 'Coca-Cola'
        elif 'diet coke' in nl or 'diet cherry coke' in nl:
            cat = 'Carbonated Soft Drinks'
            brand = 'Diet Coke'
        elif 'sprite' in nl:
            cat = 'Carbonated Soft Drinks'
            brand = 'Sprite'
        elif 'dr pepper' in nl:
            cat = 'Carbonated Soft Drinks'
            brand = 'Dr Pepper'
        elif 'fanta' in nl:
            cat = 'Carbonated Soft Drinks'
            brand = 'Fanta'
        elif 'mello yello' in nl:
            cat = 'Carbonated Soft Drinks'
            brand = 'Mello Yello'
        elif "barq's" in nl:
            cat = 'Carbonated Soft Drinks'
            brand = "Barq's Root Beer"
        elif "seagram's" in nl:
            cat = 'Carbonated Soft Drinks'
            brand = "Seagram's Ginger Ale"
        elif 'java monster' in nl or 'killer brew' in nl:
            cat = 'Energy Drinks'
            brand = 'Java Monster Coffee'
        elif 'monster rehab' in nl:
            cat = 'Energy Drinks'
            brand = 'Monster Rehab'
        elif 'monster energy ultra' in nl:
            cat = 'Energy Drinks'
            brand = 'Monster Energy Ultra'
        elif 'monster energy juice' in nl:
            cat = 'Energy Drinks'
            brand = 'Monster Energy Juice'
        elif 'monster' in nl or 'mega monster' in nl:
            cat = 'Energy Drinks'
            brand = 'Monster Energy'
        elif 'reign' in nl:
            cat = 'Energy Drinks'
            brand = 'Reign Total Body Fuel'
        elif 'bang' in nl:
            cat = 'Energy Drinks'
            brand = 'Bang Energy'
        elif 'nos' in nl:
            cat = 'Energy Drinks'
            brand = 'NOS Energy'
        elif 'full throttle' in nl:
            cat = 'Energy Drinks'
            brand = 'Full Throttle'
        elif 'storm' in nl:
            cat = 'Energy Drinks'
            brand = 'Storm Energy'
        elif 'powerade power water' in nl:
            cat = 'Sports & Hydration'
            brand = 'Powerade Power Water'
        elif 'powerade' in nl:
            cat = 'Sports & Hydration'
            brand = 'Powerade'
        elif 'bodyarmor flash' in nl:
            cat = 'Sports & Hydration'
            brand = 'BODYARMOR Flash I.V.'
        elif 'bodyarmor fit' in nl:
            cat = 'Sports & Hydration'
            brand = 'BODYARMOR Fit'
        elif 'bodyarmor sportwater' in nl:
            cat = 'Bottled & Enhanced Water'
            brand = 'BODYARMOR SportWater'
        elif 'bodyarmor' in nl:
            cat = 'Sports & Hydration'
            brand = 'BODYARMOR SuperDrink & Lyte'
        elif 'smartwater' in nl:
            cat = 'Bottled & Enhanced Water'
            brand = 'smartwater'
        elif 'vitaminwater' in nl:
            cat = 'Enhanced Water & Wellness'
            brand = 'vitaminwater'
        elif 'dasani' in nl:
            cat = 'Bottled & Enhanced Water'
            brand = 'Dasani Water'
        elif 'topo chico' in nl:
            cat = 'Sparkling Water & Seltzers'
            brand = 'Topo Chico'
        elif 'minute maid' in nl:
            cat = 'Juices & Fruit Drinks'
            brand = 'Minute Maid'
        elif 'hi-c' in nl:
            cat = 'Juices & Fruit Drinks'
            brand = 'Hi-C'
        elif 'gold peak' in nl:
            cat = 'Ready-to-Drink Teas'
            brand = 'Gold Peak Tea'
        elif 'core power' in nl:
            cat = 'Dairy & Protein Drinks'
            brand = 'Core Power Protein'
        elif 'fairlife' in nl:
            cat = 'Dairy & Protein Drinks'
            brand = 'Fairlife Milk'
        elif "dunkin'" in nl:
            cat = 'Ready-to-Drink Coffee'
            brand = "Dunkin' Iced Coffee"
        elif 'tum-e' in nl:
            cat = 'Kids Drinks & Juices'
            brand = 'Tum-E Yummies'
            
        # Default package fallback if not specified
        if not pack:
            if size == '20 oz':
                pack = '24 Loose'
            elif size == '24 oz':
                pack = '24 Loose' if cat != 'Energy Drinks' else '12 Loose'
            elif size == '28 oz':
                pack = '15 Loose'
            elif size == '2 Liter':
                pack = '8 Loose'
            elif size == '1 Liter':
                pack = '12 Loose'
            elif size == '1.5 Liter':
                pack = '12 Loose'
            elif size == '23.7 oz':
                pack = '24 Loose'
            elif size == '16 oz' and ctype == 'Can':
                pack = '24 Loose'
            elif size == '12 oz' and ctype == 'Can':
                pack = '12 Pack (2 CT)'
            elif size == '7.5 oz':
                pack = '6 Pack (4 CT)'
            elif size == '8 oz':
                pack = '6 Pack (4 CT)'
            elif size == '355 mL':
                pack = '24 Loose'
            elif size == '10.1 oz':
                pack = '12 Loose'
            elif size == '13.7 oz' or size == '14 oz' or size == '15 oz':
                pack = '12 Loose'
                
        catalog.append({
            'id': f"drink-{sku}",
            'sku': sku,
            'upc': upc,
            'category': cat,
            'brand_group': brand,
            'full_name': name,
            'size': size,
            'container_type': ctype,
            'packaging': pack,
            'image_path': f"drink_images/sku_{sku}.png"
        })
        
    return catalog

cat = build_drink_catalog()
cat.sort(key=lambda x: (x['category'], x['brand_group'], x['full_name'], x['size']))

with open('catalog.json', 'w') as f:
    json.dump(cat, f, indent=2)

print(f"Catalog created with {len(cat)} items in catalog.json")
