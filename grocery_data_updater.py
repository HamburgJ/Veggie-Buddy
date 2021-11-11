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

# Get data
asession = AsyncHTMLSession(workers=200)

results = []
to_run = []
for city, postal_code in postal_codes.items():
    to_run = to_run + [lambda store=store,
                              city=city, 
                              postal_code=postal_code, 
                              session=asession: get_data(store, postal_code, city, session) for store in websites]

r = asession.run( *to_run)
for data in r:
    results.append(data)

nltk.download('wordnet')
df = pd.concat(results)

# Preprocessing
df['category'] = df['category'].str[9:]
df['name'] = [ftfy.fix_text(str(x).lower()) for x in df['name']]
df['price'] = [ftfy.fix_text(str(x).lower()) for x in df['price']]
df['story'] = [ftfy.fix_text(str(x).lower()) for x in df['story']]

for key, value in name_replacements.items():
    df['name'] = [x.replace(key, value) for x in df['name']]

for key, value in price_replacements.items():
    df['price'] = [x.replace(key, value) for x in df['price']]

df.dropna(subset=['price', 'story'], inplace=True)

# Fix categories to be consistant across stores
categories = []

for category in df['category']:
    if category not in category_dict.keys():
        categories.append('delete')
    else:
        categories.append(category_dict[category])


df['category'] = categories
df = df[df['category'] != 'delete']

df.reset_index(inplace=True,drop=True)
df.drop_duplicates(inplace=True, subset=['name','price','store','location'])
df.reset_index(inplace=True,drop=True)

categories = df['category']
# Detect items with meat or vegan keywords and fix categories
df['vegan'] = ["FALSE" for x in range(len(df.index))]

######################## SOMETHING WRONG WITH THIS EVERYTHING GOES TO MEAT--- LOOK AT THE DICTS
for i in range(len(df.index)):
    for category, dictionary in keyword_categories.items():
        for keyword in dictionary:
            if hasword(df['name'][i], [keyword]):
                categories[i] = category
#################################
# Fix pricing info

df['category'] = categories
prices = [0 for x in range(len(df.index))]

for i in range(len(df.index)):
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
df['real_price'] = prices 

df['foods'] = [[] for x in range(len(df.index))]
df['food categories'] = [[] for x in range(len(df.index))]

lemmatizer = WordNetLemmatizer()

# Detect individual food items
# This is done because some item contain multiple different products,
# so multiple products may be split off from one item
for i in range(len(df.index)):
    name = df['name'][i]
    if (df['category'][i] in ["produce", "other"]):
        for food in produce_keywords:
            if (hasword(name, [food]) or
                hasword(lemmatizer.lemmatize(name), [food]) or
                hasword(name, lemmatizer.lemmatize(name))):
                df['foods'][i].append(food)
                df['food categories'][i].append('produce')
        
        for food, dictionary in complex_match_produce.items():
            if hasword(name, dictionary['positive'], dictionary['negative']):
                df['foods'][i].append(food)
                df['food categories'][i].append('produce')
    
    for food, dictionary in complex_match_foods.items():
        if hasword(name, dictionary['positive'], dictionary['negative']):
            df['foods'][i].append(food)
            df['food categories'][i].append(dictionary['category'])
    
# If no products are found in an item, the product will just be the item name
for i in range(len(df.index)):
    if df['foods'][i] == []:
        df['foods'][i] = [df['name'][i]]
        df['food categories'][i] = [df['category'][i]]

# Create new df based on products
rows = []
row_food_labels = []
category_labels = []
for i in range(len(df.index)):
    for j in range(len(df['foods'][i])):
        rows.append(df.iloc[i])
        row_food_labels.append(df['foods'][i][j])
        category_labels.append(df['food categories'][i][j])

final_df = pd.DataFrame(rows, columns=['name','price','store','image','story','vegan','foods','real_price','location'])
final_df['name'] = [x.capitalize() for x in final_df['name']]
final_df.insert(loc=0, column="category", value=category_labels)
final_df.insert(loc=0, column="item", value=row_food_labels)
final_df.sort_values(inplace=True, by=['real_price'])
final_df.reset_index(drop=True,inplace=True)

# To avoid incorrect images from multi-items, choose the image from the item with the fewest products detected
for i in range(len(row_food_labels)):
    item_df = pd.DataFrame(final_df.loc[final_df['item'] == row_food_labels[i]], columns = ['foods','image'])
    item_df.reset_index(inplace=True, drop=True)
    if len(item_df) > 1:
        shortest = 0
        for j in range(len(item_df)):   
            if (len(item_df['foods'][j]) < len(item_df['foods'][shortest])):
                shortest = j

        # Fix special-case images for items that are commonly only in multi-items
        if len(item_df['foods'][shortest]) > 1 and row_food_labels[i] in ['avocados', 'blackberries', 'strawberries', 'raspberries', 'blueberries', 'plums']:
            final_df.loc[final_df['item'] == row_food_labels[i], 'image'] = "../static/images/" + str(row_food_labels[i]) + ".png"
        else:
            final_df.loc[final_df['item'] == row_food_labels[i], 'image'] = item_df['image'][shortest]

# Connect to MongoDB
#client =  MongoClient(os.environ['MONGODB_URI'])
#db = client['groceryDatabase']
#collection = db['groceryCollection']
#data_dict = final_df.to_dict("records")

# Reset and Insert collection
#collection.delete_many({})
#collection.insert_many(data_dict)
final_df.to_csv('yeah.csv')
print('Grocery data update complete!')
