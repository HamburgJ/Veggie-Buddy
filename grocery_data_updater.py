import pandas as pd
import re
import ftfy
import os
from nltk.stem import WordNetLemmatizer
import nltk
from requests_html import AsyncHTMLSession
from pymongo import MongoClient
from constants import *
from updater_functions import *

# Data
category_map = pd.read_csv('category map.csv')

asession = AsyncHTMLSession()

results = []

to_run = []
for city, postal_code in postal_codes.items():
    to_run = to_run + [lambda store=store, city=city, postal_code=postal_code: get_data(store, postal_code, city) for store in websites]

r = asession.run( *to_run)
for data in r:
    results.append(data)

nltk.download('wordnet')
df = pd.concat(results)

# Preprocessing
df['category'] = df['category'].str[9:]
df['name'] = [ftfy.fix_text(str(x).lower()).replace("®","").replace('mangos', "mangoes").replace("sweet potatoes", "yams").replace("jalapeño pepper", "jalepeno").replace('chili pepper','chili').replace('clementine', 'orange').replace('mandarin','orange').replace('salads','salad') for x in df['name']]
df['price'] = [ftfy.fix_text(str(x).lower()).replace("¢", "").replace('or less than 2', 'or').replace('or less than 3', 'or').replace('or less than 4', 'or').replace('or less than 5', 'or').replace('or less than 6', 'or').replace('less than 2', 'or').replace('less than 3', 'or').replace('less than 4', 'or').replace('less than 5', 'or').replace('less than 6', 'or').replace('each', 'ea.').replace(' ea.', "").replace(' or /lb', "").replace('/lb', 'lb').replace(" .", " $0.").replace(' ea', '').replace(" for", "/").replace(' ealb', '').replace('lb.','lb') for x in df['price']]
df['story'] = [ftfy.fix_text(str(x).lower()) for x in df['story']]
df.dropna(subset=['price', 'story'], inplace=True)

# Fix categories to be consistant across stores
group1s = []
group2s = []
cats = list(category_map['category'])
for category in df['category']:
    if category not in cats:
        group1s.append('delete')
        group2s.append('delete')
    else:
        line = category_map[category_map['category'] == category].index[0]
        group1s.append(category_map['group2'][line])
        group2s.append(category_map['group1'][line])

df['category'] = group1s
df['category 2'] = group2s
df = df[df['category'] != 'delete']

df.reset_index(inplace=True,drop=True)
df.drop_duplicates(inplace=True, subset=['name','price','store','location'])
df.reset_index(inplace=True,drop=True)


# Detect items with meat or vegan keywords and fix categories
df['vegan'] = ["FALSE" for x in range(0, len(df.index))]

for i in range(len(df.index)-1):
    for keyword in meat_keywords:
        if re.search('(?:(?<=\s)|(?<=^))'+keyword+'(?=\s|$|,)', df['name'][i]):
            df['category 2'][i] = 'meat'

    for keyword in vegan_keywords:
        if re.search('(?:(?<=\s)|(?<=^))'+keyword+'(?=\s|$|,)', df['name'][i]):
            df['category 2'][i] = 'vegan'


# Fix pricing info
prices = [0 for x in range(len(df.index))]
for i in range(0, len(df.index)):
    string = df['price'][i]
    deal = re.search("([0-9])\s?(?:\/|for)\s\$([0-9]+.[0-9][0-9])", string)
    if deal:
        prices[i] = float(deal.group(2))/float(deal.group(1))
    else:
        p = re.search("\$([0-9]+.[0-9][0-9])", string)
        if string.find('lb')>-1:
            prices[i] = 100000
        if p:
            prices[i] = prices[i] + float(p.group(1))
        else:
            prices[i] = 10000000000
df['real price'] = prices 

df['foods'] = [[] for x in range(0, len(df.index))]
df['food categories'] = [[] for x in range(0, len(df.index))]

lemmatizer = WordNetLemmatizer()

# Detect individual food items
# This is done because some item contain multiple different products, so multiple products may be split off from one item
for i in range(0, len(df.index)):
    name = df['name'][i]
    if (df['category 2'][i] == "produce") or (df['store'][i] in ['Food Basics','Giant Tiger'] and df['category 2'][i] == 'none'):
        for food in foods:
            if (re.search('(?:(?<=\s)|(?<=^))'+food+'(?=\s|$|,)', name) or
                re.search('(?:(?<=\s)|(?<=^))'+lemmatizer.lemmatize(food)+'(?=\s|$|,)', name) or
                re.search('(?:(?<=\s)|(?<=^))'+food+'(?=\s|$|,)', lemmatizer.lemmatize(name))):
                df['foods'][i].append(food)
                df['food categories'][i].append('produce')
        
        if hasword(name, ['grapes'], ['tomato','tomatoes']):
            df['foods'][i].append('grapes')
            df['food categories'][i].append('produce')
        if hasword(name, ['grape tomato', 'grape tomatoes'], ['salad']):
            df['foods'][i].append('grape tomatoes')
            df['food categories'][i].append('produce')
        if hasword(name, ['tomatoes', 'tomato'], ['grape', 'grapes', 'salad', 'canned', 'rotel', 'crushed', 'paste', 'sauce', 'sauce']):
            df['foods'][i].append('tomatoes')
            df['food categories'][i].append('produce')
    
    #becel
    if hasword(name, ['becel']):
        df['foods'][i].append('becel')
        df['food categories'][i].append('vegan')
    #coffee
    if hasword(name, ['coffee','roast and ground','maxwell house','nabob bag']):
        df['foods'][i].append('coffee')
        df['food categories'][i].append('other')
    #milk
    if hasword(name, ['coconut dream','silk','blue diamond','almond milk','oat yeah','soy milk','soy beverage','almond beverage','oat beverage','oat milk','almond milk', 'cashew milk'], ['becel', 'pudding']):
        df['foods'][i].append('nut milk')
        df['food categories'][i].append('vegan')
    #coke
    if hasword(name, ['coke','pepsi','cola','soft drink','soda'], ['soda water']):
        df['foods'][i].append('cola')
        df['food categories'][i].append('other')
    #chips
    if hasword(name, ['chips','smartfood','cheetos','bugels','doritos','lays','corn chips'], ['chocolate chips','carob chips']):
        df['foods'][i].append('chips')
        df['food categories'][i].append('other')
    #popcorn
    if hasword(name, ['popcorn', 'smartfood', 'bad monkey']):
        df['foods'][i].append('popcorn')
        df['food categories'][i].append('other')
    #crackers
    if hasword(name, ['crackers', 'triscuit','wheat thins','crispers','ritz','saltine','saltines']):
        df['foods'][i].append('crackers')
        df['food categories'][i].append('other')
    
    if hasword(name, ['cereal', 'cereals', 'general mills','shreddies','post'],['oatmeal']):
        df['foods'][i].append('cereal')
        df['food categories'][i].append('other')

    if hasword(name, ['oatmeal', 'oats'], ['of oats']):
        df['foods'][i].append('oats')
        df['food categories'][i].append('other')
    
    if hasword(name, ['chocolate', 'chocolates'], ['chocolate milk', 'chocolate ice','chocolate cream','chocolate pastry']):
        df['foods'][i].append('chocolate')
        df['food categories'][i].append('other')
    
    if hasword(name, ['dressing', 'dressings']):
        df['foods'][i].append('salad dressing')
        df['food categories'][i].append('other')

    if hasword(name, ['salad', 'salads'], ['dressing', 'dressings', 'fruit salad', 'salad mix', 'pasta salad']):
        df['foods'][i].append('salad')
        df['food categories'][i].append('produce')
    
    if hasword(name, ['corn'], ['beef', 'chip', 'tortilla', 'chips', 'tortillas', 'popping']):
        df['foods'][i].append('corn')
        df['food categories'][i].append('produce')

    if hasword(name, ['onion', 'onions'], ['green onion', 'green onions', 'red onion', 'red onions']):
        df['foods'][i].append('onion')
        df['food categories'][i].append('produce')
    elif hasword(name, ['green onion', 'green onions']):
        df['foods'][i].append('green onion')
        df['food categories'][i].append('produce')
    elif hasword(name, ['red onion', 'red onions']):
        df['foods'][i].append('red onion')
        df['food categories'][i].append('produce')

    if hasword(name, ['green bean', 'green beans', 'long beans', 'fresh beans', 'french beans'], ['canned', 'pickled']):
        df['foods'][i].append('green beans')
        df['food categories'][i].append('produce')

    if hasword(name, ['romaine', 'lettuce'], ['salad', 'wrap']):
        df['foods'][i].append('lettuce')
        df['food categories'][i].append('produce')

    if hasword(name, ['yams', 'sweet potato', 'yam', 'sweet potato'], ['sauce', 'food', 'pie']):
        df['foods'][i].append('sweet potato')
        df['food categories'][i].append('produce')
    
    if hasword(name, ['classico', 'pasta sauce', 'prima', 'pasta sauces', 'marinara sauce', 'tomato sauce']):
        df['foods'][i].append('pasta sauce')
        df['food categories'][i].append('other')

    if hasword(name, ['fruit bowls','dole fruit']):
        df['foods'][i].append('fruit snack')
        df['food categories'][i].append('other')
    
    if hasword(name, ['peanut butter']):
        df['foods'][i].append('peanut butter')
        df['food categories'][i].append('other')

    if hasword(name, ['jam', 'jelly'], ['jellies']):
        df['foods'][i].append('jam')
        df['food categories'][i].append('other')

    if hasword(name, ['ketchup'], ['chips']):
        df['foods'][i].append('ketchup')
        df['food categories'][i].append('other')
    
    if hasword(name, ['mustard']):
        df['foods'][i].append('mustard')
        df['food categories'][i].append('other')
    
    if hasword(name, ['vinegar'], ['salt and', 'chips', 'crisps', 'fish', '']):
        df['foods'][i].append('vinegar')
        df['food categories'][i].append('other')
    
    if hasword(name, ['white sugar', 'brown sugar', 'icing sugar']):
        df['foods'][i].append('sugar')
        df['food categories'][i].append('other')

    if hasword(name, ['sparkling water', 'flavoured water', 'stevia water', 'fizzy water', 'bubly', 'montelliar', 'free and clear', 'carbonated water']):
        df['foods'][i].append('sparkling water')
        df['food categories'][i].append('other')

    if hasword(name, ['bagel', 'bagels'], ['hummus', 'bagel bite', 'bagel bites', 'mini', 'seasoning']):
        df['foods'][i].append('bagels')
        df['food categories'][i].append('bakery')

    if hasword(name, ['english muffins', 'english muffin'], ['maple', 'cinnamon']):
        df['foods'][i].append('english muffins')
        df['food categories'][i].append('bakery')
    
    if hasword(name, ['bread', 'loaf'], ['baguette', 'buns', 'bowl']):
        df['foods'][i].append('bread')
        df['food categories'][i].append('bakery')
    
    if hasword(name, ['tortilla', 'torillas'], ['chips','seasoning', 'hard', 'fried']):
        df['foods'][i].append('tortillas')
        df['food categories'][i].append('bakery')
    
    if hasword(name, ['hummus']):
        df['foods'][i].append('hummus')
        df['food categories'][i].append('vegan')
    
    if hasword(name, ['mixed nuts', 'nut mix', 'premium nuts', 'deluxe nuts']):
        df['foods'][i].append('mixed nuts')
        df['food categories'][i].append('other')

    if hasword(name, ['cookies', 'cookie', 'oreo', 'chips ahoy', 'voortman']):
        df['foods'][i].append('cookies')
        df['food categories'][i].append('bakery')
    
    if hasword(name, ['olive oil', 'canola oil', 'corn oil', 'vegetable oil', 'seed oil'], ['hummus', 'chips', 'olives', 'tomatoes']):
        df['foods'][i].append('oil')
        df['food categories'][i].append('other')

    if hasword(name, ['broth']):
        df['foods'][i].append('broth')
        df['food categories'][i].append('other')
    
    if hasword(name, ['pickles', 'gherkins'], ['chips', 'flavour']):
        df['foods'][i].append('pickles')
        df['food categories'][i].append('other')
    
    if hasword(name, ['buns']):
        df['foods'][i].append('buns')
        df['food categories'][i].append('bakery')

    if hasword(name, ['canned tomato', 'canned tomatoes', 'rotel', 'tomato paste', 'crushed tomato']):
        df['foods'][i].append('canned tomato')
        df['food categories'][i].append('other')
    
    if hasword(name, ['salsa']):
        df['foods'][i].append('salsa')
        df['food categories'][i].append('other')
    
    if hasword(name, ['tofu'], ['dip']):
        df['foods'][i].append('tofu')
        df['food categories'][i].append('vegan')
    
    if hasword(name, ['waffles', 'waffle', 'eggo'], ['beglian']):
        df['foods'][i].append('waffles')
        df['food categories'][i].append('other')

    if hasword(name, ['orange', 'oranges'], ['segments', 'canned', 'syrup', 'candy', 'popcicles', 'chicken', 'sauce', 'juice', 'pekoe', 'drink', 'tropicana', 'soda', 'pop', 'sodas', 'sparkling', 'cookie', 'cookies', 'pulp', 'pure', 'marmalade', 'water','fanta', 'tic tac', 'zevia', 'gatorade', 'peel', 'crush', 'jelly', 'jam', 'jello', 'powder', 'crystals', 'tang', 'bar', 'soap', 'shampoo', 'chocolate']):
        df['foods'][i].append('oranges')
        df['food categories'][i].append('produce')
    
# If no products are found in an item, the product will just be the item name
for i in range(0, len(df.index)):
    if df['foods'][i] == []:
        df['foods'][i] = [df['name'][i]]
        df['food categories'][i] = [df['category 2'][i]]

# Create new df based on products
rows = []
row_food_labels = []
category_labels = []
for i in range(0, len(df.index)):
    for j in range(len(df['foods'][i])):
        rows.append(df.iloc[i])
        row_food_labels.append(df['foods'][i][j])
        category_labels.append(df['food categories'][i][j])

final_df = pd.DataFrame(rows, columns=['name','price','store','image','story','vegan','foods','real price','location'])
final_df['name'] = [x.capitalize() for x in final_df['name']]
final_df.insert(loc=0, column="category", value=category_labels)
final_df.insert(loc=0, column="item", value=row_food_labels)
final_df.sort_values(inplace=True, by=['real price'])
final_df.reset_index(drop=True,inplace=True)

# To avoid incorrect images from multi-items, choose the image from the item with the fewest products detected
for i in range(0,len(row_food_labels)):
    item_df = pd.DataFrame(final_df.loc[final_df['item'] == row_food_labels[i]], columns = ['foods','image'])
    item_df.reset_index(inplace=True, drop=True)
    if len(item_df) > 1:
        shortest = 0
        for j in range(0, len(item_df)):   
            if (len(item_df['foods'][j]) < len(item_df['foods'][shortest])):
                shortest = j

        # Fix special-case images for items that are commonly only in multi-items
        if len(item_df['foods'][shortest]) > 1 and row_food_labels[i] in ['avocados', 'blackberries', 'strawberries', 'raspberries', 'blueberries', 'plums']:
            final_df.loc[final_df['item'] == row_food_labels[i], 'image'] = "../static/images/" + str(row_food_labels[i]) + ".png"
        else:
            final_df.loc[final_df['item'] == row_food_labels[i], 'image'] = item_df['image'][shortest]

# Connect to MongoDB
'''
client =  MongoClient(os.environ['MONGODB_URI'])
db = client['groceryDatabase']
collection = db['groceryCollection']
data_dict = final_df.to_dict("records")

# Reset and Insert collection
collection.delete_many({})
collection.insert_many(data_dict)
'''
final_df.to_csv('grocery data processed.csv')

print('Grocery data update complete!')
