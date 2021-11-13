import re
from constants import *
import pandas as pd
import time
from requests_html import AsyncHTMLSession
from pymongo import MongoClient
import os
import ftfy
from nltk.stem import WordNetLemmatizer
import nltk

pd.options.mode.chained_assignment = None

# Checks if any of the postitive words are in the string and none of the negative are
def has_word(string, positive, negative=[]):
    if negative != []:
        if re.search('(?:(?<=\s)|(?<=^))('+ '|'.join(negative)+')(?=\s|$|,)', string):
            return False
    if re.search('(?:(?<=\s)|(?<=^))('+ '|'.join(positive)+')(?=\s|$|,)', string):
        return True
    return False

# Processing website item data to dataframe
async def get_data(store, postal_code, city, session):
    params = {
        'postal_code': postal_code,
        'locale' : 'en',
        'type' : 1
    }
    #print('getting a data')
    start = time.time()
    try:
        r = await session.get(websites[store], params=params)
        category = 2
        rows = []
        while len(r.html.xpath('//*[@id="wrapper"]/div[8]/div/div[2]/div[' + str(category) + ']')) != 0:
            category_name = r.html.xpath('//*[@id="wrapper"]/div[8]/div/div[2]/div[' + str(category) + ']')[0].attrs['class'][0]

            imgs = [x.attrs['src'] for x in r.html.xpath('//*[@id="wrapper"]/div[8]/div/div[2]/div[' + str(category) + ']/ul/li/div[1]/div/a/img')]
            prices = [x.text for x in r.html.xpath('//*[@id="wrapper"]/div[8]/div/div[2]/div[' + str(category) + ']/ul/li/div[3]')]                                                        
            stories = [x.text.replace('nan', "") for x in r.html.xpath('//*[@id="wrapper"]/div[8]/div/div[2]/div[' + str(category) + ']/ul/li/div[2]')]
            names = [x.text for x in r.html.xpath('//*[@id="wrapper"]/div[8]/div/div[2]/div[' + str(category) + ']/ul/li/div[4]')]
            this_stores = [store for x in range(len(imgs))]
            categories = [category_name for x in range(len(imgs))]
            this_locations = [city for x in range(len(imgs))]

            column_dict = {
                'name' : names,
                'price' : prices,
                'store': this_stores,
                'image' : imgs,
                'story' : stories,
                'category': categories,
                'location': this_locations
            }

            rows.append(pd.DataFrame(column_dict))
            category += 1

        print('done. time took: {} link: {} postal: {}'.format(time.time() - start, websites[store], postal_code))

        if len(rows) > 0:
            store_data = pd.concat(rows)
            return store_data
    except:
        pass

    return pd.DataFrame()

def delete_items():
    client =  MongoClient(os.environ['MONGODB_URI'])
    db = client['groceryDatabase']
    for city in postal_codes.keys():
        collection = db[str(city)]
        collection.delete_many({})

    client.close()

def process(df):
    if len(df.index) == 0:
        return
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

    # Detect items with meat or vegan keywords and fix categories
    df['vegan'] = ["FALSE" for x in range(len(df.index))]

    # Sort to categories by keyword
    categories = df['category']

    for i in range(len(df.index)):
        for category, dictionary in keyword_categories.items():
            for keyword in dictionary:
                if has_word(df['name'][i], [keyword]):
                    categories[i] = category

    df['category'] = categories

    # Fix pricing info
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
                if (has_word(name, [food]) or
                    has_word(lemmatizer.lemmatize(name), [food]) or
                    has_word(name, [lemmatizer.lemmatize(food)])):
                    df['foods'][i].append(food)
                    df['food categories'][i].append('produce')
            
            for food, dictionary in complex_match_produce.items():
                if has_word(name, dictionary['positive'], dictionary['negative']):
                    df['foods'][i].append(food)
                    df['food categories'][i].append('produce')

        for food, dictionary in complex_match_foods.items():
            if has_word(name, dictionary['positive'], dictionary['negative']):
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

    if len(df.index)==0:
        return
        
    # Connect to MongoDB
    client =  MongoClient(os.environ['MONGODB_URI'])
    db = client['groceryDatabase']

    collection = db[str(df['location'][0])]
    data_dict = final_df.to_dict("records")

    # Insert
    collection.insert_many(data_dict)

    client.close()