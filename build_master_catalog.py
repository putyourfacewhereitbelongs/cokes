import json
import re

with open('catalog.json') as f:
    items = json.load(f)

# Specific refinements on items
corrections = {
    '412633': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy Ultra',
        'full_name': 'Monster Energy Ultra Fantasy Ruby Red Zero Sugar',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '413893': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy',
        'full_name': 'Monster Energy Reserve Orange Dreamsicle',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '414176': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy Juice',
        'full_name': 'Monster Energy Juice Strawberry Lemonade',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '413270': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy Ultra',
        'full_name': 'Monster Energy Ultra Blue Hawaiian Zero Sugar',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '414121': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy Ultra',
        'full_name': 'Monster Energy Ultra Red White & Blue Razz Zero Sugar',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '412024': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy Ultra',
        'full_name': 'Monster Energy Ultra Strawberry Dreams Zero Sugar',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '412031': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy Ultra',
        'full_name': 'Monster Energy Ultra Strawberry Dreams Zero Sugar',
        'size': '12 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '413894': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy Ultra',
        'full_name': 'Monster Energy Ultra Wild Passion Zero Sugar',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '413998': {
        'category': 'Energy Drinks',
        'brand_group': 'Reign Total Body Fuel',
        'full_name': 'Reign Total Body Fuel Watermelon Sour Gummy',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '154900': {
        'category': 'Juices & Fruit Drinks',
        'brand_group': 'Minute Maid',
        'full_name': 'Minute Maid Juice-To-Go 100% Apple Juice',
        'size': '12 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '24 Loose'
    },
    '154898': {
        'category': 'Juices & Fruit Drinks',
        'brand_group': 'Minute Maid',
        'full_name': 'Minute Maid Juice-To-Go 100% Orange Juice',
        'size': '12 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '24 Loose'
    },
    '154899': {
        'category': 'Juices & Fruit Drinks',
        'brand_group': 'Minute Maid',
        'full_name': 'Minute Maid Juice-To-Go 100% Pineapple Orange Juice',
        'size': '12 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '24 Loose'
    },
    '154914': {
        'category': 'Juices & Fruit Drinks',
        'brand_group': 'Minute Maid',
        'full_name': 'Minute Maid Juice-To-Go Cranberry Apple Raspberry',
        'size': '12 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '24 Loose'
    },
    '154915': {
        'category': 'Juices & Fruit Drinks',
        'brand_group': 'Minute Maid',
        'full_name': 'Minute Maid Juice-To-Go Cranberry Grape',
        'size': '12 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '24 Loose'
    },
    '412570': {
        'category': 'Sparkling Water & Seltzers',
        'brand_group': 'Topo Chico',
        'full_name': 'Topo Chico Sabores Blueberry with Hibiscus',
        'size': '12 oz',
        'container_type': 'Can',
        'packaging': '8 Pack'
    },
    '412571': {
        'category': 'Sparkling Water & Seltzers',
        'brand_group': 'Topo Chico',
        'full_name': 'Topo Chico Sabores Tangerine with Ginger',
        'size': '12 oz',
        'container_type': 'Can',
        'packaging': '8 Pack'
    },
    '413881': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR Flash I.V.',
        'full_name': 'BODYARMOR Flash I.V. Zero Sugar Caffeine Pineapple Passionfruit',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '413880': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR Flash I.V.',
        'full_name': 'BODYARMOR Flash I.V. Zero Sugar Caffeine Watermelon Punch',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '413820': {
        'category': 'Sports & Hydration',
        'brand_group': 'Powerade Power Water',
        'full_name': 'Powerade Power Water Zero Sugar Mountain Berry Blast',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '24 Loose'
    },
    '413819': {
        'category': 'Sports & Hydration',
        'brand_group': 'Powerade Power Water',
        'full_name': 'Powerade Power Water Zero Sugar Tropical Pineapple',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '24 Loose'
    },
    '413818': {
        'category': 'Sports & Hydration',
        'brand_group': 'Powerade Power Water',
        'full_name': 'Powerade Power Water Zero Sugar Watermelon',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '24 Loose'
    },
    '413821': {
        'category': 'Sports & Hydration',
        'brand_group': 'Powerade Power Water',
        'full_name': 'Powerade Power Water Zero Sugar Strawberry Kiwi',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '24 Loose'
    },
    '414169': {
        'category': 'Energy Drinks',
        'brand_group': 'Storm Energy',
        'full_name': 'Storm Zero Sugar Guava Strawberry',
        'size': '12 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '414168': {
        'category': 'Energy Drinks',
        'brand_group': 'Storm Energy',
        'full_name': 'Storm Zero Sugar Harvest Grape',
        'size': '12 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '414167': {
        'category': 'Energy Drinks',
        'brand_group': 'Storm Energy',
        'full_name': 'Storm Zero Sugar Tropical',
        'size': '12 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '414166': {
        'category': 'Energy Drinks',
        'brand_group': 'Storm Energy',
        'full_name': 'Storm Zero Sugar Valencia Orange',
        'size': '12 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '414141': {
        'category': 'Energy Drinks',
        'brand_group': 'NOS Energy',
        'full_name': 'NOS Energy Gran Prix Guava',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '414001': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy Ultra',
        'full_name': 'Monster Energy Ultra Punk Punch Zero Sugar',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '413146': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy Ultra',
        'full_name': 'Monster Energy Ultra Vice Guava Zero Sugar',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '414009': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy',
        'full_name': 'Monster Energy Lando Norris Zero Sugar',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '413994': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy',
        'full_name': 'Monster Energy Strawberry Shot',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '413995': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy',
        'full_name': 'Monster Energy Strawberry Shot Zero Sugar',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '414021': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy Juice',
        'full_name': 'Monster Energy Juice Voodoo Grape',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '413895': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy Juice',
        'full_name': 'Monster Energy Juice Bad Apple',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '413305': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy Juice',
        'full_name': 'Monster Energy Juice Viking Berry',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '412701': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy Juice',
        'full_name': 'Monster Energy Juice Rio Punch',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '413892': {
        'category': 'Energy Drinks',
        'brand_group': 'Monster Energy',
        'full_name': 'Monster Energy Electric Blue',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '24 Loose'
    },
    '412591': {
        'category': 'Energy Drinks',
        'brand_group': 'Reign Total Body Fuel',
        'full_name': 'Reign Total Body Fuel Sour Gummy Worm',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '411461': {
        'category': 'Energy Drinks',
        'brand_group': 'Reign Total Body Fuel',
        'full_name': 'Reign Total Body Fuel Reignbow Sherbet',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '157135': {
        'category': 'Energy Drinks',
        'brand_group': 'Reign Total Body Fuel',
        'full_name': 'Reign Total Body Fuel Orange Dreamsicle',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '410704': {
        'category': 'Energy Drinks',
        'brand_group': 'Reign Total Body Fuel',
        'full_name': 'Reign Total Body Fuel White Gummy Bear',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '413225': {
        'category': 'Energy Drinks',
        'brand_group': 'Reign Total Body Fuel',
        'full_name': 'Reign Total Body Fuel White Haze',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '410703': {
        'category': 'Energy Drinks',
        'brand_group': 'Reign Total Body Fuel',
        'full_name': 'Reign Total Body Fuel Cherry Limeade',
        'size': '16 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '412900': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR Flash I.V.',
        'full_name': 'BODYARMOR Flash I.V. Zero Sugar Lemon Lime',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '412342': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR Flash I.V.',
        'full_name': 'BODYARMOR Flash I.V. Grape',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '412340': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR Flash I.V.',
        'full_name': 'BODYARMOR Flash I.V. Orange',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '412345': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR Flash I.V.',
        'full_name': 'BODYARMOR Flash I.V. Strawberry Kiwi',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '412344': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR Flash I.V.',
        'full_name': 'BODYARMOR Flash I.V. Tropical Punch',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '414129': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR Fit',
        'full_name': 'BODYARMOR Fit Citrus Grapefruit',
        'size': '12 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '414133': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR Fit',
        'full_name': 'BODYARMOR Fit Mixed Berry',
        'size': '12 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '414134': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR Fit',
        'full_name': 'BODYARMOR Fit Orange Mango',
        'size': '12 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '414130': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR Fit',
        'full_name': 'BODYARMOR Fit Tropical Passionfruit',
        'size': '12 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '414131': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR Fit',
        'full_name': 'BODYARMOR Fit Watermelon Lime',
        'size': '12 oz',
        'container_type': 'Can',
        'packaging': '12 Loose'
    },
    '412515': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR SuperDrink & Lyte',
        'full_name': 'BODYARMOR SuperDrink Strawberry Banana',
        'size': '28 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '15 Loose'
    },
    '412527': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR SuperDrink & Lyte',
        'full_name': 'BODYARMOR SuperDrink Strawberry Grape',
        'size': '28 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '15 Loose'
    },
    '412534': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR SuperDrink & Lyte',
        'full_name': 'BODYARMOR SuperDrink Tropical Passionfruit',
        'size': '28 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '15 Loose'
    },
    '412521': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR SuperDrink & Lyte',
        'full_name': 'BODYARMOR SuperDrink Tropical Punch',
        'size': '28 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '15 Loose'
    },
    '412532': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR SuperDrink & Lyte',
        'full_name': 'BODYARMOR SuperDrink Blue Raspberry',
        'size': '28 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '15 Loose'
    },
    '412520': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR SuperDrink & Lyte',
        'full_name': 'BODYARMOR SuperDrink Fruit Punch',
        'size': '28 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '15 Loose'
    },
    '412516': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR SuperDrink & Lyte',
        'full_name': 'BODYARMOR SuperDrink Orange Mango',
        'size': '28 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '15 Loose'
    },
    '412529': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR SuperDrink & Lyte',
        'full_name': 'BODYARMOR LYTE Peach Mango',
        'size': '28 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '15 Loose'
    },
    '413539': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR SuperDrink & Lyte',
        'full_name': 'BODYARMOR Zero Sugar Fruit Punch',
        'size': '28 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '15 Loose'
    },
    '413538': {
        'category': 'Sports & Hydration',
        'brand_group': 'BODYARMOR SuperDrink & Lyte',
        'full_name': 'BODYARMOR Zero Sugar Lemon Lime',
        'size': '28 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '15 Loose'
    },
    '156845': {
        'category': 'Sports & Hydration',
        'brand_group': 'Powerade',
        'full_name': 'Powerade Strawberry Lemonade',
        'size': '28 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '15 Loose'
    },
    '413547': {
        'category': 'Sports & Hydration',
        'brand_group': 'Powerade',
        'full_name': 'Powerade Xtra Sour Peach Pucker',
        'size': '28 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '15 Loose'
    },
    '413902': {
        'category': 'Sports & Hydration',
        'brand_group': 'Powerade',
        'full_name': 'Powerade Xtra Sour Green Apple',
        'size': '28 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '15 Loose'
    },
    '156085': {
        'category': 'Enhanced Water & Wellness',
        'brand_group': 'vitaminwater',
        'full_name': 'vitaminwater Essential (Orange-Orange)',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '156088': {
        'category': 'Enhanced Water & Wellness',
        'brand_group': 'vitaminwater',
        'full_name': 'vitaminwater Zero Sugar Power-C (Dragonfruit)',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '156079': {
        'category': 'Enhanced Water & Wellness',
        'brand_group': 'vitaminwater',
        'full_name': 'vitaminwater Zero Sugar Squeezed (Lemonade)',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '156078': {
        'category': 'Enhanced Water & Wellness',
        'brand_group': 'vitaminwater',
        'full_name': 'vitaminwater Zero Sugar XXX (Acai-Blueberry-Pomegranate)',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '413163': {
        'category': 'Enhanced Water & Wellness',
        'brand_group': 'vitaminwater',
        'full_name': 'vitaminwater Zero Sugar Re-Hydrate (Strawberry Kiwi)',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '413158': {
        'category': 'Enhanced Water & Wellness',
        'brand_group': 'vitaminwater',
        'full_name': 'vitaminwater Elevate',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '156084': {
        'category': 'Enhanced Water & Wellness',
        'brand_group': 'vitaminwater',
        'full_name': 'vitaminwater Focus (Kiwi-Strawberry)',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '156090': {
        'category': 'Enhanced Water & Wellness',
        'brand_group': 'vitaminwater',
        'full_name': 'vitaminwater Power-C (Dragonfruit)',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '156091': {
        'category': 'Enhanced Water & Wellness',
        'brand_group': 'vitaminwater',
        'full_name': 'vitaminwater Energy (Tropical Citrus)',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '156082': {
        'category': 'Enhanced Water & Wellness',
        'brand_group': 'vitaminwater',
        'full_name': 'vitaminwater Refresh (Tropical Mango)',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '156089': {
        'category': 'Enhanced Water & Wellness',
        'brand_group': 'vitaminwater',
        'full_name': 'vitaminwater XXX (Acai-Blueberry-Pomegranate)',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '411690': {
        'category': 'Bottled & Enhanced Water',
        'brand_group': 'smartwater',
        'full_name': 'smartwater Alkaline with Antioxidants',
        'size': '1 Liter',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '411713': {
        'category': 'Bottled & Enhanced Water',
        'brand_group': 'smartwater',
        'full_name': 'smartwater Alkaline with Antioxidants',
        'size': '1.5 Liter',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '411691': {
        'category': 'Bottled & Enhanced Water',
        'brand_group': 'smartwater',
        'full_name': 'smartwater Alkaline with Antioxidants',
        'size': '23.7 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '24 Loose'
    },
    '129252': {
        'category': 'Bottled & Enhanced Water',
        'brand_group': 'smartwater',
        'full_name': 'smartwater Pure Distilled Water',
        'size': '1 Liter',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '129253': {
        'category': 'Bottled & Enhanced Water',
        'brand_group': 'smartwater',
        'full_name': 'smartwater Pure Distilled Water',
        'size': '1.5 Liter',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '129254': {
        'category': 'Bottled & Enhanced Water',
        'brand_group': 'smartwater',
        'full_name': 'smartwater Pure Distilled Water',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '24 Loose'
    },
    '132296': {
        'category': 'Bottled & Enhanced Water',
        'brand_group': 'smartwater',
        'full_name': 'smartwater Pure Distilled Water',
        'size': '23.7 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '24 Loose'
    },
    '156137': {
        'category': 'Bottled & Enhanced Water',
        'brand_group': 'BODYARMOR SportWater',
        'full_name': 'BODYARMOR SportWater Alkaline & Electrolytes',
        'size': '23.7 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '24 Loose'
    },
    '156136': {
        'category': 'Bottled & Enhanced Water',
        'brand_group': 'BODYARMOR SportWater',
        'full_name': 'BODYARMOR SportWater Alkaline & Electrolytes',
        'size': '1 Liter',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '112260': {
        'category': 'Bottled & Enhanced Water',
        'brand_group': 'Dasani Water',
        'full_name': 'Dasani Purified Water',
        'size': '1 Liter',
        'container_type': 'Plastic Bottle',
        'packaging': '12 Loose'
    },
    '112259': {
        'category': 'Bottled & Enhanced Water',
        'brand_group': 'Dasani Water',
        'full_name': 'Dasani Purified Water',
        'size': '20 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '24 Loose'
    },
    '116366': {
        'category': 'Bottled & Enhanced Water',
        'brand_group': 'Dasani Water',
        'full_name': 'Dasani Purified Water',
        'size': '16.9 oz',
        'container_type': 'Plastic Bottle',
        'packaging': '24 Pack Case'
    },
    '126582': {
        'category': 'Carbonated Soft Drinks',
        'brand_group': 'Fanta',
        'full_name': 'Fanta Orange de Mexico (Glass Bottle)',
        'size': '355 mL',
        'container_type': 'Glass Bottle',
        'packaging': '24 Loose'
    },
    '122360': {
        'category': 'Carbonated Soft Drinks',
        'brand_group': 'Coca-Cola',
        'full_name': 'Coca-Cola de Mexico (Glass Bottle)',
        'size': '355 mL',
        'container_type': 'Glass Bottle',
        'packaging': '24 Loose'
    },
    '126583': {
        'category': 'Carbonated Soft Drinks',
        'brand_group': 'Sprite',
        'full_name': 'Sprite de Mexico (Glass Bottle)',
        'size': '355 mL',
        'container_type': 'Glass Bottle',
        'packaging': '24 Loose'
    },
    '413914': {
        'category': 'Carbonated Soft Drinks',
        'brand_group': 'Coca-Cola',
        'full_name': 'Coca-Cola Original Taste (Glass Bottle)',
        'size': '8 oz',
        'container_type': 'Glass Bottle',
        'packaging': '6 Pack (4 CT)'
    },
    '129137': {
        'category': 'Carbonated Soft Drinks',
        'brand_group': 'Coca-Cola',
        'full_name': 'Coca-Cola Zero Sugar (Glass Bottle)',
        'size': '8 oz',
        'container_type': 'Glass Bottle',
        'packaging': '6 Pack (4 CT)'
    },
    '413943': {
        'category': 'Carbonated Soft Drinks',
        'brand_group': 'Sprite',
        'full_name': 'Sprite Lemon-Lime (Glass Bottle)',
        'size': '8 oz',
        'container_type': 'Glass Bottle',
        'packaging': '6 Pack (4 CT)'
    },
}

for it in items:
    sku = it['sku']
    if sku in corrections:
        c = corrections[sku]
        it.update(c)

# Clean any residual comma or formatting
for it in items:
    it['full_name'] = re.sub(r'[,.\-_:;]+$', '', it['full_name']).strip()
    if not it['size'] and '16 oz' in it['full_name']:
        it['size'] = '16 oz'
    if not it['packaging']:
        if it['size'] == '20 oz': it['packaging'] = '24 Loose'
        elif it['size'] == '28 oz': it['packaging'] = '15 Loose'
        elif it['size'] == '16 oz' and it['container_type'] == 'Can': it['packaging'] = '24 Loose'
        elif it['size'] == '12 oz' and it['container_type'] == 'Can': it['packaging'] = '12 Pack (2 CT)'
        elif it['size'] == '2 Liter': it['packaging'] = '8 Loose'

# Sort by Category, Brand Group, Full Name, Size
items.sort(key=lambda x: (x['category'], x['brand_group'], x['full_name'], x['size']))

with open('final_drinks_master.json', 'w') as f:
    json.dump(items, f, indent=2)

print(f"Master drinks database saved with {len(items)} items in final_drinks_master.json")
