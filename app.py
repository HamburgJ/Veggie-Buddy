from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import pandas as pd
import random
import requests
import gevent.pywsgi
import os
from static_data import *
from constants import *
from functions import has_word

app = Flask(__name__)

def get_location():
    if request.method == 'POST':
        return request.form.get('city_select')

    arg_location = request.args.get('location')
    if arg_location is not None:
        return arg_location
    return 'kingston'
    ip = request.environ['HTTP_X_FORWARDED_FOR']
    r = requests.get('https://ipinfo.io/{}/json'.format(ip))
    json = r.json()
    client_location = json['city']
    city = client_location.lower().replace(' ','-').replace('.','')

    return city 

@app.route('/', methods=['GET', 'POST'])
def home():
    search = None
    if request.method == 'POST':
        search = request.form.get('search_query')

        stores = []
        for store in websites.keys():
            storeData = request.form.get('has_{}'.format(store))
            if storeData is None:
                continue
            if not storeData == 'on':
                continue
            stores.append(store)
        
        categories = []
        category_list =  list(set(category_dict.values()))
        for category in category_list:
            categoryData = request.form.get('has_{}'.format(category))
            if categoryData is None:
                continue
            if not categoryData == 'on':
                continue
            categories.append(category)

    city = get_location()

    client =  MongoClient(os.environ['MONGODB_URI'])
    db = client['groceryDatabase']
    collection = db[city]

    df = pd.DataFrame(list(collection.find()))
    
    
    #Search
    if not search is None:
        searched_df = df.drop(df[has_word(df['name'], [search])].index)
        if len(searched_df.index) > 0:
            df = searched_df
        else:
            message = 'search not found'

    ipcity = 'guelph'

    #df = pd.DataFrame(list(data))

    # Fix NaN data
    df['story'] = [ str(x).replace("nan", "") for x in df['story']]
    df['price'] = [ str(x).replace("nan", "") for x in df['price']]

    # Reformat data to list of dfs
    items = list(set(df['item']))
    colnum = 5
    dfs = [[] for x in range(colnum)]
    lengths = [0 for x in range(colnum)]

    for i in range(0,len(items)):
        new_df = pd.DataFrame(df.loc[df['item'] == items[i]], columns=['item','name','price','store','image','story','category','vegan','foods'])
        insert = lengths.index(min(lengths))
        lengths[insert] = lengths[insert] + 3 + len(new_df.index)
        dfs[insert].append(new_df)

    row_datas = [[list(d.values.tolist()) for d in df] for df in dfs]

    city_stores = list(set(df['store']))
    categories = list(set(category_dict.values()))
    kwargs = {
        'row_datas': row_datas,
        'column_names': df.columns.tolist(),
        'link_column': "image",
        'zip': zip, 
        'city': city, 
        'ipcity': ipcity, 
        'cities': cities_formatted,
        'stores': city_stores,
        'categories': categories
    }

    return render_template('main.html', **kwargs)

app_server = gevent.pywsgi.WSGIServer(('0.0.0.0', int(os.environ.get("PORT", 5000))), app)
app_server.serve_forever()