import json
import re

with open('products_to_review.json') as f:
    products = json.load(f)

def clean_item(p):
    sku = p['sku']
    upc = p['upc']
    raw = p['raw_cleaned']
    
    # Clean raw string
    s = raw
    s = re.sub(r'^(Add\s*to\s*Cart|AddtoCart|Add toCart|\+|\-|\×|\中|\十|\–|\*)\s*', '', s, flags=re.IGNORECASE)
    s = re.sub(r'\s*(Add\s*to\s*Cart|AddtoCart|Add toCart|\+|\-|\×|\中|\十|\–|\*)$', '', s, flags=re.IGNORECASE)
    s = re.sub(r'^\s*[,.\-_:;]+\s*', '', s)
    s = re.sub(r'\s*[,.\-_:;]+$', '', s)
    
    # Custom special SKUs
    custom_map = {
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
    }
    
    if sku in custom_map:
        cat, brand, name, size, ctype, pack = custom_map[sku]
        return {
            'sku': sku,
            'upc': upc,
            'category': cat,
            'brand_group': brand,
            'full_name': name,
            'size': size,
            'container_type': ctype,
            'packaging': pack,
            'image_path': f'drink_images/sku_{sku}.png',
            'raw': raw
        }
        
    # Extract packaging
    pack = ''
    if re.search(r'12\s*pk\s*[,，]?\s*2\s*ct', s, re.IGNORECASE):
        pack = '12 Pack (2 CT)'
    elif re.search(r'15\s*pk\s*[,，]?\s*2\s*ct', s, re.IGNORECASE):
        pack = '15 Pack (2 CT)'
    elif re.search(r'6\s*pk\s*[,，]?\s*4\s*ct', s, re.IGNORECASE):
        pack = '6 Pack (4 CT)'
    elif re.search(r'4\s*pk\s*[,，]?\s*6\s*ct', s, re.IGNORECASE):
        pack = '4 Pack (6 CT)'
    elif re.search(r'8\s*pk', s, re.IGNORECASE):
        pack = '8 Pack'
    elif re.search(r'24\s*pk', s, re.IGNORECASE):
        pack = '24 Pack Case'
    elif re.search(r'24\s*(?:loose|lo0se)', s, re.IGNORECASE):
        pack = '24 Loose'
    elif re.search(r'12\s*(?:loose|lo0se)', s, re.IGNORECASE):
        pack = '12 Loose'
    elif re.search(r'15\s*(?:loose|lo0se)', s, re.IGNORECASE):
        pack = '15 Loose'
    elif re.search(r'8\s*(?:loose|lo0se)', s, re.IGNORECASE):
        pack = '8 Loose'
    elif 'bag-in-box' in s.lower():
        pack = '1 Box'
        
    # Extract size
    size_pat = r'(\b\d+(?:\.\d+)?\s*(?:oz|ltr|Itr|liter|L|gal|ml|g|G)\b|\b\d+(?:\.\d+)?(?=oz|ltr|Itr|liter|L|gal|ml)(?:oz|ltr|Itr|liter|L|gal|ml)\b)'
    size_m = re.search(size_pat, s, re.IGNORECASE)
    size = size_m.group(1) if size_m else ''
    
    # Normalize size
    if size:
        size = re.sub(r'(?i)itr', 'Liter', size)
        size = re.sub(r'(?i)ltr', 'Liter', size)
        size = re.sub(r'(?i)liter', 'Liter', size)
        size = re.sub(r'(\d+)\s*(?:Liter|L)', r'\1 Liter', size)
        size = re.sub(r'(\d+(?:\.\d+)?)\s*oz', r'\1 oz', size)
        size = re.sub(r'(\d+(?:\.\d+)?)\s*ml', r'\1 mL', size)
        size = re.sub(r'(\d+(?:\.\d+)?)\s*gal', r'\1 Gal', size)
        size = size.strip()
        
    # Container type
    ctype = 'Plastic Bottle'
    if 'can' in s.lower() or 'cans' in s.lower():
        ctype = 'Can'
    elif 'bag-in-box' in s.lower():
        ctype = 'Bag-in-Box'
    elif 'mexico' in s.lower() or '355' in s or '8 oz bottle' in s.lower():
        ctype = 'Glass Bottle'
    elif 'cup' in s.lower():
        ctype = 'Cup'
        
    # Strip size and packaging from title
    name_clean = s
    # Split before size pattern if exists
    if size_m:
        name_clean = s[:size_m.start()].strip()
    # Strip trailing commas
    name_clean = re.sub(r'[,.\-_:;]+$', '', name_clean).strip()
    
    # Format words cleanly
    name_clean = re.sub(r'([a-z])([A-Z])', r'\1 \2', name_clean)
    name_clean = re.sub(r'([A-Za-z])(\d)', r'\1 \2', name_clean)
    name_clean = re.sub(r'(\d)([A-Za-z])', r'\1 \2', name_clean)
    name_clean = re.sub(r'\s+', ' ', name_clean).strip()
    
    # Fix specific brand names & flavours
    name_clean = re.sub(r'Coca - Cola', 'Coca-Cola', name_clean)
    name_clean = re.sub(r'Coca Cola', 'Coca-Cola', name_clean)
    name_clean = re.sub(r'DrPepper', 'Dr Pepper', name_clean)
    name_clean = re.sub(r'Dr Pepper', 'Dr Pepper', name_clean)
    name_clean = re.sub(r'DietDrPepper', 'Diet Dr Pepper', name_clean)
    name_clean = re.sub(r'Diet DrPepper', 'Diet Dr Pepper', name_clean)
    name_clean = re.sub(r'Diet Coke', 'Diet Coke', name_clean)
    name_clean = re.sub(r'DietCherryCoke', 'Diet Cherry Coke', name_clean)
    name_clean = re.sub(r'Diet Cherry Coke', 'Diet Cherry Coke', name_clean)
    name_clean = re.sub(r'SpriteChill', 'Sprite Chill', name_clean)
    name_clean = re.sub(r'Sprite Tropical Mix', 'Sprite Tropical Mix', name_clean)
    name_clean = re.sub(r'SpriteZeroSugar', 'Sprite Zero Sugar', name_clean)
    name_clean = re.sub(r'Barqs', "Barq's", name_clean)
    name_clean = re.sub(r'MelloYello', 'Mello Yello', name_clean)
    name_clean = re.sub(r'Seagrams', "Seagram's", name_clean)
    name_clean = re.sub(r'Glaceau Smartwater', 'smartwater', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Glaceau Vitaminwater', 'vitaminwater', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Glaceausmartwater', 'smartwater', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Glaceauvitaminwater', 'vitaminwater', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'MinuteMaid', 'Minute Maid', name_clean)
    name_clean = re.sub(r'Powerade', 'Powerade', name_clean)
    name_clean = re.sub(r'Bodyarmor', 'BODYARMOR', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Reign Total Body Fuel', 'Reign Total Body Fuel', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'ReignTotalBodyFuel', 'Reign Total Body Fuel', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Bang Energy', 'Bang Energy', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'BangEnergy', 'Bang Energy', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Monster Energy', 'Monster Energy', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'MonsterEnergy', 'Monster Energy', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Gold Peak', 'Gold Peak', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'GoldPeak', 'Gold Peak', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Fairlife Milk', 'Fairlife Milk', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'FairlifeMilk', 'Fairlife Milk', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Core Power', 'Core Power', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'CorePower', 'Core Power', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r"Dunkin'", "Dunkin'", name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Topo Chico', 'Topo Chico', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Tum - E Yummies', 'Tum-E Yummies', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Tum-EYummies', 'Tum-E Yummies', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Storm Zero Sugar', 'Storm Zero Sugar', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'StormZeroSugar', 'Storm Zero Sugar', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Nos Energy', 'NOS Energy', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Nos', 'NOS', name_clean)
    name_clean = re.sub(r'Full Throttle', 'Full Throttle', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'FullThrottle', 'Full Throttle', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Dasani', 'Dasani', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Hi - C', 'Hi-C', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'Hi-C', 'Hi-C', name_clean, flags=re.IGNORECASE)
    
    # Specific fixups
    replacements = [
        (r'Coca-Cola Cherry Zero\b', 'Coca-Cola Cherry Zero Sugar'),
        (r'Coca-Cola ZeroSugar\b', 'Coca-Cola Zero Sugar'),
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
        (r'Dunkin\' French Vanilla lced Coffee\b', "Dunkin' French Vanilla Iced Coffee"),
        (r'Dunkin\' Mocha Iced Coffee\b', "Dunkin' Mocha Iced Coffee"),
        (r'Dunkin\' Original Iced Coffee\b', "Dunkin' Original Iced Coffee"),
        (r'Dunkin\' Caramel Iced Coffee\b', "Dunkin' Caramel Iced Coffee"),
        (r'Dunkin\' Double Original Iced Espresso\b', "Dunkin' Double Espresso - Original"),
        (r'Dunkin\' Double Cafe Mocha Iced Espresso\b', "Dunkin' Double Espresso - Cafe Mocha"),
        (r'Gold Peak Extra Sweet Tea\b', 'Gold Peak Extra Sweet Tea'),
        (r'Gold Peak Sweetened Black Tea\b', 'Gold Peak Sweetened Black Tea'),
        (r'Gold Peak Sweetened Green Tea\b', 'Gold Peak Sweetened Green Tea'),
        (r'Gold Peak Unsweetened Black Tea\b', 'Gold Peak Unsweetened Black Tea'),
        (r'Gold Peak Zero Sugar Sweet Tea\b', 'Gold Peak Zero Sugar Sweet Tea'),
        (r'Core Power Protein Vanilla Elite 42 G\b', 'Core Power Protein Vanilla Elite 42g'),
        (r'Core Power Protein Strawberry Elite 42 G\b', 'Core Power Protein Strawberry Elite 42g'),
        (r'Core Power Protein Chocolate Elite 42 G\b', 'Core Power Protein Chocolate Elite 42g'),
        (r'Core Power Protein Chocolate 26 G\b', 'Core Power Protein Chocolate 26g'),
        (r'Core Power Protein Vanilla 26 G\b', 'Core Power Protein Vanilla 26g'),
        (r'Core Power Protein Strawberry Banana 26 G\b', 'Core Power Protein Strawberry Banana 26g'),
        (r'Fairlife Milk 2% Reduced Fat\b', 'Fairlife 2% Reduced Fat Ultra-Filtered Milk'),
        (r'Fairlife Milk 2% Chocolate\b', 'Fairlife 2% Chocolate Ultra-Filtered Milk'),
        (r'Fairlife Milk 2% Strawberry\b', 'Fairlife 2% Strawberry Ultra-Filtered Milk'),
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
        (r'Monster Killer Brew Mean Bean\b', 'Monster Killer Brew Mean Bean'),
        (r'Monster Killer Brew Loca Moca\b', 'Monster Killer Brew Loca Moca'),
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
        (r'Full Throttle\b', 'Full Throttle Original'),
        (r'Storm Zero Sugar Guava Strawberry\b', 'Storm Zero Sugar Guava Strawberry'),
        (r'Storm Zero Sugar Harvest Grape\b', 'Storm Zero Sugar Harvest Grape'),
        (r'Storm Zero Sugar Tropical\b', 'Storm Zero Sugar Tropical'),
        (r'Storm Zero Sugar Valencia Orange\b', 'Storm Zero Sugar Valencia Orange'),
        (r'BODYARMOR Superdrink Strawberry Banana\b', 'BODYARMOR SuperDrink Strawberry Banana'),
        (r'BODYARMOR Superdrink Strawberry Grape\b', 'BODYARMOR SuperDrink Strawberry Grape'),
        (r'BODYARMOR Superdrink Tropical Passionfruit\b', 'BODYARMOR SuperDrink Tropical Passionfruit'),
        (r'BODYARMOR Superdrink Tropical Punch\b', 'BODYARMOR SuperDrink Tropical Punch'),
        (r'BODYARMOR Superdrink Blue Raspberry\b', 'BODYARMOR SuperDrink Blue Raspberry'),
        (r'BODYARMOR Superdrink Fruit Punch\b', 'BODYARMOR SuperDrink Fruit Punch'),
        (r'BODYARMOR Superdrink Orange Mango\b', 'BODYARMOR SuperDrink Orange Mango'),
        (r'BODYARMOR Lyte Peach Mango\b', 'BODYARMOR LYTE Peach Mango'),
        (r'BODYARMOR Zero Sugar Fruit Punch\b', 'BODYARMOR Zero Sugar Fruit Punch'),
        (r'BODYARMOR Zero Sugar Lemon Lime\b', 'BODYARMOR Zero Sugar Lemon Lime'),
        (r'BODYARMOR Flash IV Zero Sugar Caffeine Watermelon P\b', 'BODYARMOR Flash I.V. Zero Sugar Caffeine Watermelon Punch'),
        (r'BODYARMOR Flash IV Zero Sugar Caffeine Pineapple Pa\b', 'BODYARMOR Flash I.V. Zero Sugar Caffeine Pineapple Passionfruit'),
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
        (r'BODYARMOR Sportwater\b', 'BODYARMOR SportWater Alkaline & Electrolytes'),
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
        name_clean = re.sub(pat, rep, name_clean, flags=re.IGNORECASE)
        
    name_clean = re.sub(r'\s+', ' ', name_clean).strip()
    name_clean = re.sub(r'[,.\-_:;]+$', '', name_clean).strip()
    
    # Categorization and Brand Group
    brand_group = 'Other'
    cat = 'Other Beverages'
    
    nl = name_clean.lower()
    
    if 'coca-cola' in nl or 'mexico' in nl and 'coca' in nl:
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
    elif 'java monster' in nl:
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
        
    # If name is just the brand name itself, add Original Taste / Classic
    if name_clean == 'Coca-Cola':
        name_clean = 'Coca-Cola Original Taste'
    elif name_clean == 'Diet Coke':
        name_clean = 'Diet Coke Classic'
    elif name_clean == 'Sprite':
        name_clean = 'Sprite Lemon-Lime'
    elif name_clean == 'Dr Pepper':
        name_clean = 'Dr Pepper Original'
    elif name_clean == 'Barqs Root Beer' or name_clean == "Barq's Root Beer":
        name_clean = "Barq's Root Beer"
    elif name_clean == 'Mello Yello':
        name_clean = 'Mello Yello Citrus'
    elif name_clean == 'Dasani':
        name_clean = 'Dasani Purified Water'
    elif name_clean == 'smartwater':
        name_clean = 'smartwater Pure Distilled Water'
    elif name_clean == 'Full Throttle':
        name_clean = 'Full Throttle Original Citrus'
    elif name_clean == 'NOS Energy':
        name_clean = 'NOS High Performance Energy'
    elif name_clean == 'Monster Energy':
        name_clean = 'Monster Energy Original (Green)'
        
    return {
        'sku': sku,
        'upc': upc,
        'category': cat,
        'brand_group': brand_group,
        'full_name': name_clean,
        'size': size,
        'container_type': ctype,
        'packaging': pack,
        'image_path': f'drink_images/sku_{sku}.png',
        'raw': raw
    }

refined = [clean_item(p) for p in products]

with open('refined_drinks.json', 'w') as f:
    json.dump(refined, f, indent=2)

print(f"Refined {len(refined)} drinks!")
