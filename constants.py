websites = {
    'Food Basics': 'https://ecirculaire.foodbasics.ca/flyers/foodbasics-flyer/grid_view/661019',
    'FreshCo': 'https://flyers.freshco.com/flyers/freshco-flyer/grid_view/656515',
    'Metro':  'https://ecirculaire.metro.ca/flyers/metro-flyer/grid_view/663149',
    'Loblaws': 'https://flyers.loblaws.ca/flyers/loblaws-dryrun/grid_view/650023',
    'No Frills': 'https://flyers.nofrills.ca/flyers/nofrills-weeklyflyer/grid_view/650453',
    'Giant Tiger': 'https://eflyers.gianttiger.com/flyers/gianttiger-weeklyflyer/grid_view/650424',
    'Walmart': 'https://flyers.walmart.ca/flyers/walmartcanada-groceryflyer/grid_view/651584',
    'Shoppers Drug Mart': 'https://flyers.shoppersdrugmart.ca/flyers/shoppersdrugmart/grid_view/650453',
    'Real Canadian Superstore': 'https://flyers.realcanadiansuperstore.ca/flyers/realcanadiansuperstore/grid_view/650453',
    'Sobeys': 'https://flyers.sobeys.com/flyers/sobeys-flyer/grid_view/656515',
    'Foodland': 'https://flyers.sobeys.com/flyers/foodland-flyer/grid_view/660825',
    'Zehrs': 'https://flyers.zehrs.ca/flyers/zehrs-weeklyflyer/grid_view/650155',
    'Fortinos': 'https://flyers.fortinos.ca/flyers/fortinos-dryrun/grid_view/650044',
    'Valumart': 'https://flyers.valumart.ca/flyers/valumart-dryrun/grid_view/650044',
    'T&T': 'https://flyers.loblaws.ca/flyers/tntsupermarket-dryrun/grid_view/650044',
    'Freshmart': 'https://flyers.loblaws.ca/flyers/freshmart-dryrun/grid_view/650044',
    'Independent': 'https://flyers.loblaws.ca/flyers/yourindependentgrocer-dryrun/grid_view/650044',
    'Super C': 'https://ecirculaire.metro.ca/flyers/superc-flyer/grid_view/663149',
    'Extra Foods': 'https://flyers.loblaws.ca/flyers/extrafoods-dryrun/grid_view/650044',
    'Farm Boy': 'https://flyers.sobeys.com/flyers/farmboy-flyer/grid_view/656515',
    'Longos': 'https://flyers.sobeys.com/flyers/longos-flyer/grid_view/656515'
}

stores = websites.keys()
owned_by_loblaws = [
    'Loblaws',
    'No Frills',
    'Shoppers Drug Mart',
    'Real Canadian Superstore',
    'Zehrs',
    'T&T',
    'Independent',
    'Freshmart',
    'Valumart'
]

owned_by_metro = [
    'Food Basics',
    'Metro',
    'Super C'
]

owned_by_empire = [
    'Farm Boy',
    'Freshco',
    'Longos',
    'Sobeys',
    'Foodland'
]

name_replacements = {
    "®": "",
    'mangos': "mangoes",
    "sweet potatoes": "yams",
    "jalapeño pepper": "jalepeno",
    'chili pepper': 'chili',
    'clementine': 'orange',
    'mandarin': 'orange',
    'salads': 'salad' 
}

price_replacements = {
    "¢": "",
    'or less than 2': 'or',
    'or less than 3': 'or',
    'or less than 4': 'or',
    'or less than 5': 'or',
    'or less than 6': 'or',
    'less than 2': 'or',
    'less than 3': 'or',
    'less than 4': 'or',
    'less than 5': 'or',
    'less than 6': 'or',
    'each': 'ea.',
    ' ea.': "",
    ' or /lb': "",
    '/lb': 'lb',
    " .": " $0.",
    ' ea': '',
    " for": "/",
    ' ealb': '',
    'lb.': 'lb'
}

vegan_keywords = [
    'violife',
    'daiya',
    'gardein',
    'silk',
    'yves', 
    'just plant', 
    'plant egg', 
    'just egg', 
    'plant based', 
    'beefless', 
    'cheese-style', 
    'chickenless',
    'beyond meat', 
    'sol cuisine', 
    'earths own', 
    'blue diamond', 
    'boca', 
    'sunrise soya',  
    'sunrise soft', 
    'lightlife',
    'field roast', 
    'so delicious', 
    'oat yeah', 
    'not milk',
    'plant-based', 
    'plant based', 
    'vegan', 
    'vegetalien', 
    'tofu', 
    'wholly veggie', 
    'zoglos', 
    'tempeh',
    'almond milk', 
    'seitan', 
    'veggie ground', 
    'veggie meat', 
    'meat replacement',
    "chick'n", 
    'vio life', 
    'unmeatable', 
    'nut cheese', 
    'cashew cheese', 
    'cashew spread', 
    'big mountain',
    'tofurky',
    'chao',
    'sweets from the earth',
    'earth island',
    'cashew dip',
    'zhoug',
    'crabless',
    'fishless',
    'miyokos',
    "miyoko's",
    'miyoko',
    'nuts for cheese',
    'fauxmagerie',
    'vegetarian',
    'non-dairy',
    'dairy free',
    'nuts for butter',
    'becel',
    'beyond burger',
    'beyond sausage',
    'beyond chicken',
    'beyond ground',
    'beyond beef',
    'meatless',
    'impossible'
]

meat_keywords = [
    'salami',
    'turkey',
    'sardines',
    'quiche',
    'cheese',
    'salmon',
    'bacon',
    'beef',
    'chicken',
    'ice cream',
    'milk',
    'yogurt',
    'cream',
    'egg',
    'eggs',
    'danone',
    'activia',
    'butter',
    'pizza',
    'hungry-man',
    'honey',
    'rinds',
    'cake',
    'whites',
    'fish',
    'fillets',
    'steak',
    'parlour',
    'pogo',
    'entrees'
]

dairy_keywords = [
    'iögo',
    'crema',
    'nestlé pouches',
    "i can't believe it's not butter!",
    'yop',
    'chool whip',
    'skyr',
    'cheestrings',
    'black diamond',
    'yogourt',
    'yoplait',
]

non_vegan = [
    'store made',
    'mix and match deal',
    'cheesecake',
    'pizza',
    'yoplait',
    'minigo',
    'yogurt',
    'hungry-man',
    'parmesan',
    'baby',
    'purée',
    'cheez whiz',
    'kraft dinner',
    'canned tuna',
    'online grocery'
]

foods = [
    'avocados',
    'cilantro',
    'broccoli',
    'cantaloupes',
    'cauliflower',
    'potatoes',
    'mandarins',
    'apples','cucumbers',
    'cabbages',
    'jalapeños',
    'lemons',
    'blueberries',
    'tangelos',
    'grapefruits',
    'raspberries',
    'blackberries',
    'strawberries',
    'yams',
    'dates',
    'pineapples',
    'peppers',
    'pears',
    'celery',
    'mangoes',
    'watermelons',
    'asparagus',
    'bananas',
    'peaches',
    'plums',
    'limes',
    'nectarines',
    'frozen fruit',
    'mushrooms',
    'carrots',
    'ginger',
    'garlic',
    'radishes',
    'spinach'
]

postal_codes = {
    'kingston': 'K7L3Y2',
    'guelph': 'N1E2L8',
    'ottawa': 'K2A1A1',
    'smiths-falls': 'K7A1A1',
    'cornwall': 'K6J1A1',
    'mississuaga': 'L5A1A1',
    'richmond-hill': 'L4C1A1',
    'ajax': 'L1Z1A1',
    'toronto': 'M5A1A1',
    'scarborough': 'M1B1A1',
    'etobicoke': 'M8Z1A1',
    'london': 'N6A1A1',
    'waterloo': 'N2J1A1',
    'kitchener': 'N2N1A1',
    'sault-ste-marie': 'P6B1A1',
    'thunder-bay': 'P7C1A1'
}

'''
postal_codes = {
    'Kingston': 'K7L3Y2',
    'Guelph': 'N1E2L8'
}
'''

item_match_dict = {
    "cola": {
        "category": 'other',
        "positive": [
            'coke',
            'pepsi',
            'cola',
            'soft drink',
            'soda'
        ],
        "negative": [
            'soda water'
        ]
    },
    "becel": {
        "category": 'vegan',
        "postive":[
            'becel'
        ],
        "negative": []
    },
    "coffee": {
        "category": 'other',
        "postive":[
            'coffee',
            'roast and ground',
            'maxwell house',
            'nabob'
        ],
        "negative": []
    },
    "nut milk": {
        "category": 'vegan',
        "postive":[
            'coconut dream',
            'silk',
            'blue diamond',
            'almond milk',
            'oat yeah',
            'soy milk',
            'not milk',
            'oat milk',
            'almond milk',
            'cashew milk'
            'soy beverage',
            'almond beverage',
            'oat beverage',
            'coconut beverage',
            'cashew beverage',
            'coconut milk',
            'cashew milk',
            'pea milk',
            'plant based milk',
            'plant-based milk',
            'plant milk',
        ],
        "negative": [
            'becel',
            'pudding',
        ]
    },
    "chips": {
        "category": 'other',
        "postive":[
            'chips',
            'cheetos',
            'bugels',
            'doritos',
            'lays',
            'corn chips',
            'kettle chips',
            'kettle cooked chips'
            'poppables'
        ],
        "negative": [
            'chocolate chips',
            'carob chips'
        ]
    },
    "popcorn": {
        "category": 'other',
        "postive":[
            'popcorn',
            'smartfood',
            'bad monkey',
            'caramel corn',
            'chicago corn',
            'pop corn'
        ],
        "negative": [

        ]
    },
    "crackers": {
        "category": 'other',
        "postive":[
            'crackers',
            'triscuit',
            'wheat thins',
            'crispers',
            'ritz',
            'saltine',
            'saltines',
            'cream cracker',
        ],
        "negative": []
    },
    "cereal": {
        "category": 'other',
        "postive":[
            'cereal',
            'cereals',
            'general mills',
            'shreddies',
            'post'
        ],
        "negative": [
            'oatmeal',
            'cake'
        ]
    },
    "oats": {
        "category": 'other',
        "postive":[
            'oatmeal',
            'oats'
        ],
        "negative": [
            'of oats'
        ]
    },
    "": {
        "category": '',
        "postive":[
            
        ],
        "negative": [
            
        ]
    },
    "chocolate": {
        "category": 'other',
        "postive":[
            'chocolate',
            'chocolates'
        ],
        "negative": [
            'chocolate milk',
            'chocolate ice',
            'chocolate cream',
            'chocolate cake',
            'chocolate brownie',
            'chocolate cookie',
            'chocolate pastry',
            'chocolate cereal',
            'chocolate bread',
            'chocolate bun'
        ]
    },
    "salad dressing": {
        "category": 'other',
        "postive":[
            'dressing',
            'dressings'
        ],
        "negative": []
    },
    "salad": {
        "category": 'produce',
        "postive":[
            'salad',
            'salads'
        ],
        "negative": [
            'dressing',
            'dressings',
            'fruit salad',
            'salad mix',
            'pasta salad'
        ]
    },
    "corn": {
        "category": 'produce',
        "postive":[
            'corn'
        ],
        "negative": [
            'beef',
            'chip',
            'chips',
            'tortilla',
            'tortillas',
            'popping',
            'pop',
            'cereal',
            'milk',
            'salad',
            'mix'
        ]
    },
    "onion": {
        "category": 'produce',
        "postive":[
            'onion',
            'onions'
        ],
        "negative": [
            'green onion',
            'green onions',
            'red onion',
            'red onions',
            'powder',
            'seasoning',
            'chips',
            'dip',
            'popcorn',
            'dried',
            'caramelized'
        ]
    },
    "green onion": {
        "category": 'produce',
        "postive":[
            'green onion',
            'green onions'
        ],
        "negative": [
            'powder',
            'seasoning',
            'dried',
            'popcorn',
            'chips'
        ]
    },
    "red onion": {
        "category": 'produce',
        "postive":[
            'red onion',
            'red onions'
        ],
        "negative": [
            'salad'
        ]
    },
    "green beans": {
        "category": 'produce',
        "postive":[
            'green bean',
            'green beans',
            'long beans',
            'fresh beans',
            'french beans'
        ],
        "negative": [
            'canned',
            'pickled'
        ]
    },
    "lettuce": {
        "category": 'produce',
        "postive":[
            'romaine',
            'lettuce'
        ],
        "negative": [
            'salad',
            'wrap',
            'roll',
            'sandwich'
        ]
    },
    "sweet potato": {
        "category": 'produce',
        "postive":[
            'yams',
            'sweet potato',
            'yam',
            'sweet potatoes'
        ],
        "negative": [
            'pie',
            'food',
            'sauce',
            'baby'
        ]
    },
    "pasta sauce": {
        "category": 'other',
        "postive":[
            'classico',
            'pasta sauce',
            'prima',
            'pasta sauces',
            'marinara sauce',
            'marinara sauces',
            'tomato sauce'
        ],
        "negative": []
    },
    "fruit snack": {
        "category": 'other',
        "postive":[
            'fruit bowls',
            'fruit bowl',
            'dole fruit',
            'fruit cup',
            'fruit cups',
            'applesauce'
        ],
        "negative": []
    },
    "peanut butter": {
        "category": 'other',
        "postive":[
            'peanut butter',
            'jif'
        ],
        "negative": []
    },
    "jam": {
        "category": 'other',
        "postive":[
            "jam",
            "jelly"
        ],
        "negative": [
            "jellies"
        ]
    },
    "ketchup": {
        "category": 'other',
        "postive":[
            'ketchup'
        ],
        "negative": [
            'chips',
            'chip',
        ]
    },
    "mustard": {
        "category": 'other',
        "postive":[
            'mustard'
        ],
        "negative": [
            'pretzel',
            'pretzels',
            'chip',
            'chips'
        ]
    },
    "vinegar": {
        "category": 'other',
        "postive":[
            'vinegar'
        ],
        "negative": [
            'salt and',
            'chips',
            'crisps',
            'fish'
        ]
    },
    "sugar": {
        "category": 'other',
        "postive":[
            'white sugar',
            'brown sugar',
            'icing sugar'
        ],
        "negative": [
            'oatmeal',
            'cereal',
            'cake',
            'pie'
        ]
    },
    "sparkling water": {
        "category": 'other',
        "postive":[
            'sparkling water',
            'flavoured water',
            'flavored water',
            'stevia water',
            'fizzy wayer',
            'bubly',
            'montelliar',
            'free and clear',
            'carbonated water'
        ],
        "negative": [
            'water bottle',
            'water bottles',
            'bottled water'
        ]
    },
    "bagels": {
        "category": 'bakery',
        "postive":[
            'bagel',
            'bagels'
        ],
        "negative": [
            'hummus',
            'bagel bite',
            'bagel bites',
            'seasoning',
            'mini',
            ''
        ]
    },
    "english muffins": {
        "category": 'bakery',
        "postive":[
            'english muffins',
            'english muffin'
        ],
        "negative": [
            'maple',
            'cinnamon'
        ]
    },
    "bread": {
        "category": 'bakery',
        "postive":[
            'bread',
            'loaf'
        ],
        "negative": [
            'baguette',
            'bun',
            'buns',
            'bowl'
        ]
    },
    "tortillas": {
        "category": 'bakery',
        "postive":[
            'tortilla',
            'tortillas'
        ],
        "negative": [
            'chips',
            'seasoning',
            'hard',
            'fried'
        ]
    },
    "hummus": {
        "category": 'vegan',
        "postive":[
            'hummus',
            'chickpea dip'
        ],
        "negative": []
    },
    "mixed nuts": {
        "category": 'other',
        "postive":[
            'mixed nuts',
            'nut mix',
            'premium nuts',
            'premium mixed nuts',
            'deluxe nuts',
            'deluxe mixed nuts'
        ],
        "negative": []
    },
    "cookies": {
        "category": 'bakery',
        "postive":[
            'cookies',
            'cookie',
            'oreo',
            'chips ahoy',
            'voortman'
        ],
        "negative": [
            
        ]
    },
    "oil": {
        "category": 'other',
        "postive":[
            'olive oil',
            'canola oil',
            'corn oil',
            'vegetable oil',
            'seed oil'
        ],
        "negative": [
            'hummus',
            'chips',
            'chip',
            'olives',
            'tomatoes',
            'salad',
            'mix'
        ]
    },
    "broth": {
        "category": 'other',
        "postive":[
            'broth'
        ],
        "negative": []
    },
    "pickes": {
        "category": 'other',
        "postive":[
            'pickles',
            'gherkins'
        ],
        "negative": [
            'chips',
            'flavour',
            'flavor',
            'flavored',
            'flavoured'
        ]
    },
    "buns": {
        "category": 'bakery',
        "postive":[
            'buns'
        ],
        "negative": []
    },
    "canned tomatoes": {
        "category": 'other',
        "postive":[
            'canned tomato',
            'canned tomatoes',
            'rotel',
            'tomato paste',
            'crushed tomato'
        ],
        "negative": []
    },
    "salsa": {
        "category": 'other',
        "postive":[
            'salsa'
        ],
        "negative": []
    },
    "tofu": {
        "category": 'vegan',
        "postive":[
            'tofu'
        ],
        "negative": [
            'dip',
            'noodles'
        ]
    },
    "waffles": {
        "category": 'other',
        "postive":[
            'waffles',
            'waffle',
            'eggo'
        ],
        "negative": [
            'belgian'
        ]
    },
    "oranges": {
        "category": 'produce',
        "postive":[
            'orange',
            'oranges'
        ],
        "negative": [
            'segments',
            'canned',
            'syrup',
            'candy',
            'sours',
            'gummies',
            'popcicles',
            'popcicle',
            'ice cream',
            'sauce',
            'juice',
            'pekoe',
            'drink',
            'tropicana',
            'soda',
            'pop',
            'sodas',
            'sparkling',
            'cookie',
            'cookies',
            'pulp',
            'pure',
            'marmalade',
            'water',
            'fanta',
            'tic tac',
            'zevia',
            'gatorade',
            'peel',
            'crush',
            'jelly',
            'jellies',
            'jam',
            'jello',
            'jell-o',
            'powder',
            'crystals',
            'tang',
            'bar',
            'soap',
            'shampoo',
            'chocolate'
        ]
    }
}