import json
import re

with open('parsed_drinks.json') as f:
    drinks = json.load(f)

# Let's inspect all drinks and create a master clean list
def polish_drink(d):
    sku = d['sku']
    upc = d['upc']
    raw = d['raw']
    full_name = d['full_name']
    cat = d['category']
    brand = d['brand_group']
    size = d['size']
    pack = d['packaging']
    ctype = d['container_type']
    
    # Clean up full_name text
    name = full_name
    name = re.sub(r'\s+', ' ', name).strip()
    name = re.sub(r'^(Add\s*to\s*Cart|AddtoCart|Add toCart|\+|\-|\×|\中|\十|\–|\*)\s*', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s*(Add\s*to\s*Cart|AddtoCart|Add toCart|\+|\-|\×|\中|\十|\–|\*)$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'^\s*[,.\-_:;]+\s*', '', name)
    name = re.sub(r'\s*[,.\-_:;]+$', '', name)
    
    # Specific known drink names cleaning
    replacements = [
        (r'Coca-Cola Cherry Zero\b', 'Coca-Cola Cherry Zero Sugar'),
        (r'Coca-Cola ZeroSugar\b', 'Coca-Cola Zero Sugar'),
        (r'Coca-ColaMexico\b', 'Coca-Cola de Mexico (Glass Bottle)'),
        (r'SpriteMexico\b', 'Sprite de Mexico (Glass Bottle)'),
        (r'FantaOrangeMexico\b', 'Fanta Orange de Mexico (Glass Bottle)'),
        (r'Fanta0rangeMexico\b', 'Fanta Orange de Mexico (Glass Bottle)'),
        (r'Fanta OrangeMexico\b', 'Fanta Orange de Mexico (Glass Bottle)'),
        (r'DrPepperStrawberries& Cream\b', 'Dr Pepper Strawberries & Cream'),
        (r'DrPepperCreamSoda\b', 'Dr Pepper & Cream Soda'),
        (r'DrPepperBlackberry\b', 'Dr Pepper Blackberry'),
        (r'DrPepperZeroSugar\b', 'Dr Pepper Zero Sugar'),
        (r'DietDrPepper\b', 'Diet Dr Pepper'),
        (r'DietCherryCoke\b', 'Diet Cherry Coke'),
        (r'SpriteChill\b', 'Sprite Chill'),
        (r'SpriteTropical Mix\b', 'Sprite Tropical Mix'),
        (r'SpriteZeroSugar\b', 'Sprite Zero Sugar'),
        (r'Seagrams\b', "Seagram's"),
        (r'Barqs\b', "Barq's"),
        (r'Tum-EYummies\b', 'Tum-E Yummies'),
        (r'Tum - E Yummies\b', 'Tum-E Yummies'),
        (r'Tum-EYummiesBigBerry Blast\b', 'Tum-E Yummies Big Berry Blast'),
        (r'Tum-EYummiesEdgyOrange Burst\b', 'Tum-E Yummies Edgy Orange Burst'),
        (r'Tum-EYummiesEpicApple Flip\b', 'Tum-E Yummies Epic Apple Flip'),
        (r'Tum-EYummiesFruitPunch Party\b', 'Tum-E Yummies Fruit Punch Party'),
        (r'Dunkin\'FrenchVanillalced Coffee\b', "Dunkin' French Vanilla Iced Coffee"),
        (r'Dunkin\'Mocha Iced Coffee\b', "Dunkin' Mocha Iced Coffee"),
        (r'Dunkin\'Original Iced Coffee\b', "Dunkin' Original Iced Coffee"),
        (r'Dunkin\'Caramel Iced Coffee\b', "Dunkin' Caramel Iced Coffee"),
        (r'Dunkin\'Double Original Iced Espresso\b', "Dunkin' Double Espresso - Original"),
        (r'Dunkin\'DoubleCafeMocha IcedEspresso\b', "Dunkin' Double Espresso - Cafe Mocha"),
        (r'GoldPeakExtraSweetTea\b', 'Gold Peak Extra Sweet Tea'),
        (r'GoldPeakSweetenedBlack Tea\b', 'Gold Peak Sweetened Black Tea'),
        (r'GoldPeakSweetened Green Tea\b', 'Gold Peak Sweetened Green Tea'),
        (r'GoldPeakUnsweetened Black Tea\b', 'Gold Peak Unsweetened Black Tea'),
        (r'GoldPeakZeroSugarSweet Tea\b', 'Gold Peak Zero Sugar Sweet Tea'),
        (r'GoldPeakSouthernStyleTea\b', 'Gold Peak Southern Style Tea'),
        (r'GoldPeakPremium UnsweetenedTea\b', 'Gold Peak Premium Unsweetened Tea'),
        (r'Core Power Protein Vanilla Elite42G\b', 'Core Power Protein Vanilla Elite 42g'),
        (r'Core Power Protein Strawberry Elite 42G\b', 'Core Power Protein Strawberry Elite 42g'),
        (r'Core Power Protein Chocolate Elite 42G\b', 'Core Power Protein Chocolate Elite 42g'),
        (r'CorePowerProteinChocolate 26G\b', 'Core Power Protein Chocolate 26g'),
        (r'Core Power Protein Vanilla 26G\b', 'Core Power Protein Vanilla 26g'),
        (r'Core Power Protein Strawberry Banana 26G\b', 'Core Power Protein Strawberry Banana 26g'),
        (r'Fairlife Milk 2% Reduced Fat\b', 'Fairlife 2% Reduced Fat Ultra-Filtered Milk'),
        (r'Fairlife Milk 2% Chocolate\b', 'Fairlife 2% Chocolate Ultra-Filtered Milk'),
        (r'Fairlife Milk 2% Strawberry\b', 'Fairlife 2% Strawberry Ultra-Filtered Milk'),
        (r'PoweradeMountainBerry Blast\b', 'Powerade Mountain Berry Blast'),
        (r'PoweradeFruitPunch\b', 'Powerade Fruit Punch'),
        (r'PoweradeLemonLime\b', 'Powerade Lemon Lime'),
        (r'PoweradeOrange\b', 'Powerade Orange'),
        (r'PoweradeStrawberry Lemonade\b', 'Powerade Strawberry Lemonade'),
        (r'PoweradeIslandBurst\b', 'Powerade Island Burst'),
        (r'PoweradeGrape\b', 'Powerade Grape'),
        (r'PoweradeXtraSourGreen Apple\b', 'Powerade Xtra Sour Green Apple'),
        (r'Powerade Xtra Sour Peach Pucker\b', 'Powerade Xtra Sour Peach Pucker'),
        (r'Powerade Zero Fruit Punch\b', 'Powerade Zero Fruit Punch'),
        (r'Powerade Zero Grape\b', 'Powerade Zero Grape'),
        (r'Powerade Zero Mixed Berry\b', 'Powerade Zero Mixed Berry'),
        (r'Powerade Zero Orange\b', 'Powerade Zero Orange'),
        (r'Powerade Zero Strawberry Smash\b', 'Powerade Zero Strawberry Smash'),
        (r'PoweradePowerWaterZero Sugar MountainBerryBlast\b', 'Powerade Power Water Zero Sugar Mountain Berry Blast'),
        (r'PoweradePowerWaterZero SugarStrawberryKiwi\b', 'Powerade Power Water Zero Sugar Strawberry Kiwi'),
        (r'Powerade Power Water Zero Sugar Tropical Pineapple\b', 'Powerade Power Water Zero Sugar Tropical Pineapple'),
        (r'Powerade Power Water Zero Sugar Watermelon\b', 'Powerade Power Water Zero Sugar Watermelon'),
        (r'Glaceau Vitaminwater\b', 'vitaminwater'),
        (r'Glaceauvitaminwater\b', 'vitaminwater'),
        (r'Glaceau Smartwater\b', 'smartwater'),
        (r'Glaceausmartwater\b', 'smartwater'),
        (r'vitaminwaterZero SugarPower C\b', 'vitaminwater Zero Sugar Power-C'),
        (r'vitaminwaterZero SugarSqueezed\b', 'vitaminwater Zero Sugar Squeezed (Lemonade)'),
        (r'vitaminwaterZero SugarxxX\b', 'vitaminwater Zero Sugar XXX (Acai-Blueberry-Pomegranate)'),
        (r'vitaminwaterZero Sugar Re-Hydrate\b', 'vitaminwater Zero Sugar Re-Hydrate (Strawberry Kiwi)'),
        (r'vitaminwaterFocus\b', 'vitaminwater Focus (Kiwi-Strawberry)'),
        (r'vitaminwaterPower C\b', 'vitaminwater Power-C (Dragonfruit)'),
        (r'vitaminwaterPowerC\b', 'vitaminwater Power-C (Dragonfruit)'),
        (r'vitaminwaterRefresh\b', 'vitaminwater Refresh (Tropical Mango)'),
        (r'vitaminwaterEssential\b', 'vitaminwater Essential (Orange-Orange)'),
        (r'vitaminwaterEnergy\b', 'vitaminwater Energy (Tropical Citrus)'),
        (r'vitaminwaterxxX\b', 'vitaminwater XXX (Acai-Blueberry-Pomegranate)'),
        (r'vitaminwaterElevate\b', 'vitaminwater Elevate'),
        (r'smartwaterAlkaline With Antioxidant\b', 'smartwater Alkaline with Antioxidants'),
        (r'smartwaterAlkaline WithAntioxidant\b', 'smartwater Alkaline with Antioxidants'),
        (r'MonsterEnergyUltraBlue HawaiianZeroSugar\b', 'Monster Energy Ultra Blue Hawaiian Zero Sugar'),
        (r'MonsterEnergyUltraFantasy RubyRed ZeroSugar\b', 'Monster Energy Ultra Fantasy Ruby Red Zero Sugar'),
        (r'MonsterEnergyUltraPunk PunchZeroSugar\b', 'Monster Energy Ultra Punk Punch Zero Sugar'),
        (r'MonsterEnergyUltraRed White&BlueRazzZeroSugar\b', 'Monster Energy Ultra Red White & Blue Razz Zero Sugar'),
        (r'MonsterEnergyUltra StrawberryDreamsZeroSug\b', 'Monster Energy Ultra Strawberry Dreams Zero Sugar'),
        (r'MonsterEnergyUltraVice Guava Zero Sugar\b', 'Monster Energy Ultra Vice Guava Zero Sugar'),
        (r'MonsterEnergyUltraViolet ZeroSugar\b', 'Monster Energy Ultra Violet Zero Sugar'),
        (r'MonsterEnergyUltraZero Sugar\b', 'Monster Energy Ultra Zero Sugar (White)'),
        (r'MonsterEnergyUltraPeachy KeenZeroSugar\b', 'Monster Energy Ultra Peachy Keen Zero Sugar'),
        (r'MonsterEnergyUltraSunrise\b', 'Monster Energy Ultra Sunrise Zero Sugar'),
        (r'MonsterEnergyUltraParadise\b', 'Monster Energy Ultra Paradise Zero Sugar'),
        (r'Monster EnergyUltra Wild PassionZeroSugar\b', 'Monster Energy Ultra Wild Passion Zero Sugar'),
        (r'MonsterEnergyZeroSugar\b', 'Monster Energy Zero Sugar (Green/Black)'),
        (r'MonsterEnergyJuiceMango Loco\b', 'Monster Energy Juice Mango Loco'),
        (r'MonsterEnergyJuicePacific Punch\b', 'Monster Energy Juice Pacific Punch'),
        (r'MonsterEnergyJuicePipeline Punch\b', 'Monster Energy Juice Pipeline Punch'),
        (r'MonsterEnergyJuiceRio Punch\b', 'Monster Energy Juice Rio Punch'),
        (r'MonsterEnergyJuiceViking Berry\b', 'Monster Energy Juice Viking Berry'),
        (r'MonsterEnergyJuiceVoodoo Grape\b', 'Monster Energy Juice Voodoo Grape'),
        (r'MonsterEnergyJuiceBad Apple\b', 'Monster Energy Juice Bad Apple'),
        (r'MonsterEnergyJuice StrawberryLemonade\b', 'Monster Energy Juice Aussie Style Lemonade'),
        (r'MonsterEnergyStrawberry ShotZeroSugar\b', 'Monster Energy Strawberry Shot Zero Sugar'),
        (r'MonsterEnergyStrawberry Shot\b', 'Monster Energy Strawberry Shot'),
        (r'MonsterEnergyLandoNorris ZeroSugar\b', 'Monster Energy Lando Norris Zero Sugar'),
        (r'MonsterEnergyElectricBlue\b', 'Monster Energy Electric Blue'),
        (r'MonsterNitroSuperDry\b', 'Monster Nitro Super Dry'),
        (r'MonsterImport Energy\b', 'Monster Energy Import'),
        (r'MegaMonsterEnergy\b', 'Mega Monster Energy (Resealable Cap)'),
        (r'Mega MonsterLocarbEnergy\b', 'Mega Monster Lo-Carb Energy (Resealable Cap)'),
        (r'MonsterLocarbEnergy\b', 'Monster Energy Lo-Carb (Blue)'),
        (r'MonsterKiller Brew Mean Bean\b', 'Monster Killer Brew Mean Bean'),
        (r'Monster Killer Brew Loca Moca\b', 'Monster Killer Brew Loca Moca'),
        (r'MonsterReserveOrange Dreamsicle\b', 'Monster Energy Reserve Orange Dreamsicle'),
        (r'ReignTotal BodyFuel Cherry Limeade\b', 'Reign Total Body Fuel Cherry Limeade'),
        (r'ReignTotal BodyFuel ReignbowSherbet\b', 'Reign Total Body Fuel Reignbow Sherbet'),
        (r'ReignTotal BodyFuel Sour GummyWorm\b', 'Reign Total Body Fuel Sour Gummy Worm'),
        (r'ReignTotal BodyFuel WatermelonSourGummy\b', 'Reign Total Body Fuel Watermelon Sour Gummy'),
        (r'ReignTotal BodyFuel White GummyBear\b', 'Reign Total Body Fuel White Gummy Bear'),
        (r'ReignTotal BodyFuel White Haze\b', 'Reign Total Body Fuel White Haze'),
        (r'ReignTotalBodyFuelOrange Dreamsicle\b', 'Reign Total Body Fuel Orange Dreamsicle'),
        (r'Bang Energy American Berry\b', 'Bang Energy American Berry'),
        (r'Bang Energy Any Means Orange\b', 'Bang Energy Any Means Orange'),
        (r'Bang Energy Black Cherry Vanilla\b', 'Bang Energy Black Cherry Vanilla'),
        (r'Bang Energy Blue Razz\b', 'Bang Energy Blue Razz'),
        (r'Bang Energy Cotton Candy\b', 'Bang Energy Cotton Candy'),
        (r'Bang Energy Lime Pop Drop\b', 'Bang Energy Lime Pop Drop'),
        (r'Bang EnergyPeach Mango\b', 'Bang Energy Peach Mango'),
        (r'Bang Energy Purple Haze\b', 'Bang Energy Purple Haze'),
        (r'BangEnergyStarBlast\b', 'Bang Energy Star Blast'),
        (r'Nos Energy\b', 'NOS Energy Original'),
        (r'Nos Gt Grape\b', 'NOS Energy GT Grape'),
        (r'NosGtGrape\b', 'NOS Energy GT Grape'),
        (r'Nos GranPrixGuava\b', 'NOS Energy Gran Prix Guava'),
        (r'NosZero\b', 'NOS Energy Zero Sugar'),
        (r'FullThrottle RedApple\b', 'Full Throttle Red Apple'),
        (r'FullThrottle\b', 'Full Throttle Original'),
        (r'Storm Zero Sugar Guava Strawberry\b', 'Storm Zero Sugar Guava Strawberry'),
        (r'Storm Zero Sugar Harvest Grape\b', 'Storm Zero Sugar Harvest Grape'),
        (r'Storm Zero Sugar Tropical\b', 'Storm Zero Sugar Tropical'),
        (r'Storm Zero Sugar Valencia Orange\b', 'Storm Zero Sugar Valencia Orange'),
        (r'BODYARMORSuperdrink StrawberryBanana\b', 'BODYARMOR SuperDrink Strawberry Banana'),
        (r'BODYARMORSuperdrink StrawberryGrape\b', 'BODYARMOR SuperDrink Strawberry Grape'),
        (r'BODYARMORSuperdrink TropicalPassionfruit\b', 'BODYARMOR SuperDrink Tropical Passionfruit'),
        (r'BODYARMORSuperdrink TropicalPunch\b', 'BODYARMOR SuperDrink Tropical Punch'),
        (r'BODYARMORSuperdrinkBlue Raspberry\b', 'BODYARMOR SuperDrink Blue Raspberry'),
        (r'BODYARMORSuperdrinkFruit Punch\b', 'BODYARMOR SuperDrink Fruit Punch'),
        (r'BODYARMORSuperdrinkOrange Mango\b', 'BODYARMOR SuperDrink Orange Mango'),
        (r'BODYARMORLytePeachMango\b', 'BODYARMOR LYTE Peach Mango'),
        (r'BODYARMORZeroSugarFruit Punch\b', 'BODYARMOR Zero Sugar Fruit Punch'),
        (r'BODYARMORZeroSugarLemon Lime\b', 'BODYARMOR Zero Sugar Lemon Lime'),
        (r'BODYARMORFlashIVZero Sugar CaffeineWatermelonP\b', 'BODYARMOR Flash I.V. Zero Sugar Caffeine Watermelon Punch'),
        (r'BODYARMORFlashIVZero SugarCaffeinePineapplePa\b', 'BODYARMOR Flash I.V. Zero Sugar Caffeine Pineapple Passionfruit'),
        (r'BODYARMORFlashIVZero SugarLemonLime\b', 'BODYARMOR Flash I.V. Zero Sugar Lemon Lime'),
        (r'BODYARMORFlashIvGrape\b', 'BODYARMOR Flash I.V. Grape'),
        (r'BODYARMORFlashIvOrange\b', 'BODYARMOR Flash I.V. Orange'),
        (r'BODYARMORFlashIvStrawberry Kiwi\b', 'BODYARMOR Flash I.V. Strawberry Kiwi'),
        (r'BODYARMORFlashIvTropical Punch\b', 'BODYARMOR Flash I.V. Tropical Punch'),
        (r'BODYARMOR Fit Citrus Grapefruit\b', 'BODYARMOR Fit Citrus Grapefruit'),
        (r'BODYARMOR Fit Mixed Berry\b', 'BODYARMOR Fit Mixed Berry'),
        (r'BODYARMORFitOrangeMango\b', 'BODYARMOR Fit Orange Mango'),
        (r'BODYARMORFitTropical Passionfruit\b', 'BODYARMOR Fit Tropical Passionfruit'),
        (r'BODYARMORFitWatermelon Lime\b', 'BODYARMOR Fit Watermelon Lime'),
        (r'BODYARMORSportwater\b', 'BODYARMOR SportWater Alkaline & Electrolytes'),
        (r'BODYARMOR Sportwater\b', 'BODYARMOR SportWater Alkaline & Electrolytes'),
        (r'Minute Maid BlueRaspberry\b', 'Minute Maid Blue Raspberry'),
        (r'Minute Maid BerryPunch\b', 'Minute Maid Berry Punch'),
        (r'Minute Maid FruitPunch\b', 'Minute Maid Fruit Punch'),
        (r'Minute MaidKiwiStrawberry\b', 'Minute Maid Kiwi Strawberry'),
        (r'Minute Maid PineappleBurst\b', 'Minute Maid Pineapple Burst'),
        (r'Minute Maid PinkLemonade\b', 'Minute Maid Pink Lemonade'),
        (r'Minute Maid Lemonade\b', 'Minute Maid Lemonade'),
        (r'Minute MaidZeroSugar Lemonade\b', 'Minute Maid Zero Sugar Lemonade'),
        (r'Minute Maid Juice-To-Go AppleJuice100\b', 'Minute Maid Juice-To-Go 100% Apple Juice'),
        (r'Minute Maid Juice-To-Go OrangeJuice100\b', 'Minute Maid Juice-To-Go 100% Orange Juice'),
        (r'Minute Maid Juice-To-Go Pineapple Orange Juice 100\b', 'Minute Maid Juice-To-Go 100% Pineapple Orange Juice'),
        (r'Minute Maid Juice-To-Go CranberryGrape\b', 'Minute Maid Juice-To-Go Cranberry Grape'),
        (r'Minute Maid Juice-To-Go CranberryAppleRaspberry\b', 'Minute Maid Juice-To-Go Cranberry Apple Raspberry'),
        (r'Topo Chico Sabores Blueberry WithHibiscus Extract\b', 'Topo Chico Sabores Blueberry with Hibiscus'),
        (r'Topo Chico Sabores Lime With Mint Extract\b', 'Topo Chico Sabores Lime with Mint'),
        (r'Topo Chico Sabores Raspberry With Lemon\b', 'Topo Chico Sabores Raspberry with Lemon'),
        (r'Topo Chico Sabores Tangerine With Ginger Extract\b', 'Topo Chico Sabores Tangerine with Ginger'),
    ]
    
    for pat, rep in replacements:
        name = re.sub(pat, rep, name, flags=re.IGNORECASE)
        
    # Clean up any trailing commas, dots, OCR quirks
    name = re.sub(r'\s+', ' ', name).strip()
    name = re.sub(r'[,.\-_:;]+$', '', name).strip()
    
    # Unified Category & Brand Names
    if 'Coca-Cola' in brand or 'Diet Coke' in brand:
        cat = 'Carbonated Soft Drinks'
    elif 'Dr Pepper' in brand or 'Sprite' in brand or 'Fanta' in brand or 'Mello Yello' in brand or "Barq's" in brand or "Seagram's" in brand:
        cat = 'Carbonated Soft Drinks'
    elif 'Monster' in brand or 'Reign' in brand or 'Bang' in brand or 'NOS' in brand or 'Full Throttle' in brand or 'Storm' in brand:
        cat = 'Energy Drinks'
    elif 'Powerade' in brand or 'BODYARMOR' in brand:
        if 'SportWater' in brand or 'Power Water' in brand:
            cat = 'Sports & Enhanced Water'
        else:
            cat = 'Sports & Hydration'
    elif 'smartwater' in brand or 'Dasani' in brand or 'BODYARMOR SportWater' in brand:
        cat = 'Bottled & Enhanced Water'
    elif 'vitaminwater' in brand:
        cat = 'Enhanced Water & Wellness'
    elif 'Topo Chico' in brand:
        cat = 'Sparkling Water & Seltzers'
    elif 'Minute Maid' in brand or 'Hi-C' in brand:
        cat = 'Juices & Fruit Drinks'
    elif 'Gold Peak' in brand:
        cat = 'Ready-to-Drink Teas'
    elif 'Fairlife' in brand or 'Core Power' in brand:
        cat = 'Dairy & Protein Drinks'
        if 'Core Power' in brand:
            brand = 'Core Power Protein'
    elif "Dunkin'" in brand:
        cat = 'Ready-to-Drink Coffee'
    elif 'Tum-E' in brand:
        cat = 'Kids Drinks & Juices'
    elif 'Bag-in-Box' in brand or 'Cups' in brand:
        cat = 'Fountain & Supplies'
        
    # Standardize container type
    if 'Can' in ctype or 'can' in name.lower() or 'can' in raw.lower():
        ctype = 'Can'
    elif 'Bag-in-Box' in ctype or 'bag-in-box' in raw.lower() or 'Bag-in-Box' in brand:
        ctype = 'Bag-in-Box'
    elif 'Cup' in ctype or 'cup' in name.lower() or 'Cup' in brand:
        ctype = 'Cup'
    elif 'Mexico' in name or 'Glass' in name or '355 mL' in size or '8 oz' in size and ('Bottle' in raw or 'bottles' in raw):
        if '8 oz' in size:
            ctype = 'Glass Bottle'
        elif 'Mexico' in name:
            ctype = 'Glass Bottle'
        else:
            ctype = 'Plastic Bottle'
    else:
        ctype = 'Plastic Bottle'
        
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

final_drinks = [polish_drink(d) for d in drinks]

with open('final_polished_drinks.json', 'w') as f:
    json.dump(final_drinks, f, indent=2)

print(f"Saved {len(final_drinks)} polished drinks to final_polished_drinks.json")
