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
import re

app = Flask(__name__)

def get_location():
    if request.method == 'POST':
        print(request.form.get('city_select').lower().replace(" ", "-").replace(".",""))
        return request.form.get('city_select').lower().replace(" ", "-").replace(".","")

    arg_location = request.args.get('location')
    if arg_location is not None:
        return arg_location

    ip = request.environ['HTTP_X_FORWARDED_FOR']
    r = requests.get('https://ipinfo.io/{}/json'.format(ip))
    json = r.json()
    client_location = json['city']
    city = client_location.lower().replace(' ','-').replace('.','')

    return city 

@app.route('/', methods=['GET', 'POST'])
def home():
    search = ''
    if request.method == 'POST':
        search = request.form.get('search_query').lower()
        search = re.sub('[^A-Z]+', '', search, 0, re.I)
        print(search)

    city = get_location()
    city_formatted = cities_formatted_dict[city]

    client =  MongoClient(os.environ['MONGODB_URI'])
    db = client['groceryDatabase']
    collection = db[city]

    df = pd.DataFrame(list(collection.find()))

    #df = pd.DataFrame(list(data))

    # Fix NaN data
    df['story'] = [ str(x).replace("nan", "") for x in df['story']]
    df['price'] = [ str(x).replace("nan", "") for x in df['price']]

    # Reformat data to list of dfs
    items = list(set(df['item']))
    colnum = 5
    dfs = [[] for x in range(colnum)]
    lengths = [0 for x in range(colnum)]

    message = None

    #Search
    if not search == '':
        searched_items = []

        for item in items:
            if has_word(item, [search], lemmatize=True):
                searched_items.append(item)

        if not searched_items == []:
            items = searched_items

    for i in range(0,len(items)):
        new_df = pd.DataFrame(df.loc[df['item'] == items[i]], columns=['item','name','price','store','image','story','category','vegan','foods', 'real price'])
        new_df = new_df.sort_values('real price')
        insert = lengths.index(min(lengths))
        lengths[insert] = lengths[insert] + 3 + len(new_df.index)
        dfs[insert].append(new_df)

    if not search == '':
        num_results = sum([len(x) for x in dfs])
        if num_results == 0:
            message = 'No results found'
        elif num_results == 1:
            message = '1 result found'
        else:
            message = '{} results found'.format(num_results)

    row_datas = [[list(d.values.tolist()) for d in df] for df in dfs]

    city_stores = list(set(df['store']))
    categories = list(set(category_dict.values()))
    kwargs = {
        'row_datas': row_datas,
        'column_names': df.columns.tolist(),
        'link_column': "image",
        'zip': zip, 
        'city': city,  
        'cities': cities_formatted,
        'stores': city_stores,
        'categories': categories,
        'message': message,
        'searched': search,
        'city_formatted': city_formatted
    }

    return render_template('main.html', **kwargs)

app_server = gevent.pywsgi.WSGIServer(('0.0.0.0', int(os.environ.get("PORT", 5000))), app)
app_server.serve_forever()