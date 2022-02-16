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
    'Extra Foods': 'https://flyers.loblaws.ca/flyers/extrafoods-dryrun/grid_view/650044',
    'Farm Boy': 'https://flyers.sobeys.com/flyers/farmboy-flyer/grid_view/656515',
    'Longos': 'https://flyers.sobeys.com/flyers/longos-flyer/grid_view/656515'
}

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
    'impossible',
    'impossible burger',
    'plant-based'
]

meat_keywords = [
    'salami',
    'turkey',
    'sardines',
    'salmon',
    'bacon',
    'beef',
    'chicken',
    'hungry-man',
    'honey',
    'rinds',
    'cake',
    'whites',
    'fish',
    'fillets',
    'steak',
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
    'ice cream',
    'milk',
    'yogurt',
    'cream',
    'egg',
    'eggs',
    'danone',
    'activia',
    'butter',
    'quiche',
    'cheese',
    'parlour',
    'whites'
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

not_food_keywords = [
    'febreze',
    'detergent',
    'soap',
    'paper towel',
    'toilet paper',
    'cascade',
    'actionpacs',
    'advil',
    'sinus',
    'toothpaste',
    'sensodyne',
    'pronamel',
    'tablets',
    'colgate',
    'underwear',
    'bladder control',
    'poise',
    'depend',
    'baby needs',
    'live clean',
    'dove',
    'epsom',
    'lipbalm',
    'earrings',
    'garbage bags',
    'dog food',
    'cat food',
    'bird food',
    'bird seed',
    'tums',
    'antacid',
    "buckley's",
    'buckley',
    'pads',
    'liners',
    'napkins',
    'napkin',
    'cutting board',
    'utensils',
    'straws',
    'neocitran',
    'cosmetics',
    'mascara',
    'nivea',
    'toothbrush',
    'whitening',
    'axe',
    'grooming',
    'irish spring',
    'sanitizer',
    'air care',
    'mouthwash',
    'pull-ups',
    'huggies',
    'pampers',
    'training pants',
    'hair care',
    'head & shoulders',
    'lotion',
    'face care',
    'litter',
    'gillette',
    'pantene',
    'pediatric',
    'dayquil',
    'nyquil',
    'emugel',
    'voltaren',
    'hair colour',
    'colorista',
    'magic root',
    'groceries',
    'halls',
    'laundry',
    'softener',
    'dryer sheet',
    'arm & hammer',
    'vitamins',
    'tide pods',
    'gain flings!',
    'orgal care',
    'tylenol',
    'tablets',
    'scrub',
    'body wash',
    'centrum',
    'multigummies'
]

keyword_categories = {
    'vegan': vegan_keywords,
    'meat': meat_keywords,
    'dairy': dairy_keywords,
    'delete': not_food_keywords
}

produce_keywords = [
    'avocados',
    'cilantro',
    'broccoli',
    'cantaloupes',
    'cauliflower',
    'mandarins',
    'apples',
    'cucumbers',
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

cities_formatted = [
    'Barrie',
    'Belleville',
    'Brampton',
    'Brantford',
    'Burlington',
    'Cambridge',
    'Cornwall',
    'Etobicoke',
    'Guelph',
    'Hamilton',
    'Kingston',
    'Kitchener',
    'London',
    'Markham',
    'Mississuaga',
    'Niagara Falls',
    'Orilla',
    'Oshawa',
    'Ottawa',
    'Owen Sound',
    'Pembroke',
    'Peterborough',
    'Pickering',
    'Picton',
    'Richmond Hill',
    'Sarnia',
    'Sault Ste. Marie',
    'Scarborough',
    'St. Catharines',
    'St. Thomas',
    'Stratford',
    'Sudbury',
    'Thunder Bay',
    'Timmins',
    'Toronto',
    'Vaughan',
    'Waterloo',
    'Windsor',
    'Woodstock'
]

cities_formatted_dict = {}
for i in cities_formatted:
    cities_formatted_dict[i.lower().replace(' ','-').replace('.', '')]=i

'''
postal_codes = {
    'Kingston': 'K7L3Y2'
}
'''

postal_codes = {
    'kingston': 'K7L1A1',
    'waterloo': 'N2L1A1'
}

category_dict = {
    'grocery': 'other',
    'beverages': 'beverages',
    'meatanddeli': 'meat',
    'produce': 'produce',
    'dairyandcheese': 'dairy',
    'fruitandvegetables': 'produce',
    'pantry': 'other',
    'drinks': 'beverages',
    'breadandbakeryproducts': 'bakery',
    'bakery': 'bakery',
    'snacks': 'snacks',
    'dairyeggs': 'dairy',
    'fruitsvegetables': 'produce',
    'meatseafood': 'meat',
    'meat': 'meat',
    'dairy': 'dairy',
    'fishandseafood': 'meat',
    'delireadymeals': 'other',
    'deli': 'meat',
    'frozenfood': 'other',
    'coregrocery': 'other',
    'dietnutrition': 'other',
    'seafood': 'meat',
    'frozen': 'other',
    'preparedmeals': 'other',
    'snacksbeverage': 'snacks',
    'processedmeat': 'meat',
    'commercialbread': 'bakery',
    'candy': 'snacks',
    'condiments': 'other',
    'cannedfoods': 'other',
    'fruits': 'produce',
    'vegetables': 'produce',
    'juicesandbeverages': 'beverages',
    'cannedfood': 'other',
    'healthnutrition': 'other',
    'cheese': 'dairy',
    'foodbeverages': 'beverages',
    'meatfish': 'meat',
    'dairyproducts': 'dairy',
    'freshfrozen': 'other',
    'vegan': 'vegan',
    'vegetarian': 'vegan',
    'plantbased': 'vegan'
}

complex_match_produce = {
    "grapes": {
        "category": 'produce',
        "positive": [
            'grapes'
        ],
        "negative": [
            'tomato',
            'tomatoes'
        ]
    },
    "grape tomatoes": {
        "category": 'produce',
        "positive": [
            'grape tomato',
            'grape tomatoes'
        ],
        "negative": [
            'salad'
        ]
    },
    "grapes": {
        "category": 'produce',
        "positive": [
            'tomatoes',
            'tomato'
        ],
        "negative": [
            'grape',
            'grapes',
            'salad',
            'canned',
            'rotel',
            'crushed',
            'paste',
            'sauce',
            'sauces'
        ]
    }
}
complex_match_foods = {
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
        "positive": [
            'becel'
        ],
        "negative": []
    },
    "coffee": {
        "category": 'other',
        "positive": [
            'coffee',
            'roast and ground',
            'maxwell house',
            'nabob'
        ],
        "negative": []
    },
    "nut milk": {
        "category": 'vegan',
        "positive": [
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
        "positive": [
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
        "positive": [
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
        "positive": [
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
        "positive": [
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
        "positive": [
            'oatmeal',
            'oats'
        ],
        "negative": [
            'of oats'
        ]
    },
    "": {
        "category": '',
        "positive": [
            
        ],
        "negative": [
            
        ]
    },
    "chocolate": {
        "category": 'other',
        "positive": [
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
        "positive": [
            'dressing',
            'dressings'
        ],
        "negative": []
    },
    "salad": {
        "category": 'produce',
        "positive": [
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
        "positive": [
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
        "positive": [
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
        "positive": [
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
        "positive": [
            'red onion',
            'red onions'
        ],
        "negative": [
            'salad'
        ]
    },
    "green beans": {
        "category": 'produce',
        "positive": [
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
        "positive": [
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
        "positive": [
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
        "positive": [
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
        "positive": [
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
        "positive": [
            'peanut butter',
            'jif'
        ],
        "negative": []
    },
    "jam": {
        "category": 'other',
        "positive": [
            "jam",
            "jelly"
        ],
        "negative": [
            "jellies"
        ]
    },
    "ketchup": {
        "category": 'other',
        "positive": [
            'ketchup'
        ],
        "negative": [
            'chips',
            'chip',
        ]
    },
    "mustard": {
        "category": 'other',
        "positive": [
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
        "positive": [
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
        "positive": [
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
        "positive": [
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
        "positive": [
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
        "positive": [
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
        "positive": [
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
        "positive": [
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
        "positive": [
            'hummus',
            'chickpea dip'
        ],
        "negative": []
    },
    "mixed nuts": {
        "category": 'other',
        "positive": [
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
        "positive": [
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
        "positive": [
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
        "positive": [
            'broth'
        ],
        "negative": []
    },
    "pickes": {
        "category": 'other',
        "positive": [
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
        "positive": [
            'buns'
        ],
        "negative": []
    },
    "canned tomatoes": {
        "category": 'other',
        "positive": [
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
        "positive": [
            'salsa'
        ],
        "negative": []
    },
    "tofu": {
        "category": 'vegan',
        "positive": [
            'tofu'
        ],
        "negative": [
            'dip',
            'noodles'
        ]
    },
    "waffles": {
        "category": 'other',
        "positive": [
            'waffles',
            'waffle',
            'eggo'
        ],
        "negative": [
            'belgian'
        ]
    },
    "potato": {
        "category": 'produce',
        "positive": [
            'potato',
            'potatoes'
        ],
        "negative": [
            'chip',
            'mashed',
            'mash',
            'pasta',
            'starch',
            'chips',
            'frozen',
            'fries'
        ]
    },
    "oranges": {
        "category": 'produce',
        "positive": [
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