from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import pandas as pd
import random
import requests
import gevent.pywsgi
import os
from static_data import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    ip = request.environ['REMOTE_ADDR']
    print('ip')
    print(ip)
    ip2 = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print('ip2')  
    print(ip2)
    ip3 = request.remote_addr
    print('ip3')
    print(ip3)
    ip4 = request.environ['HTTP_X_FORWARDED_FOR']
    print('ip4')
    print(ip4)
    ip5 = request.environ.get('REMOTE_ADDR', request.remote_addr)  
    print('ip5')
    print(ip5)
    proxy_data = request.headers['X-Forwarded-For']
    print('proxy')
    print(proxy_data)
    print('ip_list')
    ip_list = proxy_data.split(',')
    print(ip_list)
    user_ip = ip_list[0]
    print('user_ip')
    print(user_ip)
    r = requests.get('https://ipinfo.io/{}/json'.format(ip))
    print(r)
    json = r.json()
    print(json)
    client_location = json['city']
    print(client_location)
    city = client_location.lower().replace(' ','-').replace('.','')
    print(city)

    # Get data from MongoDB
    client =  MongoClient(os.environ['MONGODB_URI'])
    db = client['groceryDatabase']
    collection = db[city]

    df = pd.DataFrame(list(collection.find()))

    # Fix NaN data
    df['story'] = [ str(x).replace("nan", "") for x in df['story']]
    df['price'] = [ str(x).replace("nan", "") for x in df['price']]

    # Reformat data to list of dfs
    items = list(set(df['item']))
    colnum = 5
    dfs = [[] for x in range(colnum)]
    lengths = [0 for x in range(colnum)]
    categories = [[] for x in range(len(items))]
    for i in range(0,len(items)):
        new_df = pd.DataFrame(df.loc[df['item'] == items[i]], columns=['item','name','price','store','image','story','category','vegan','foods'])
        insert = lengths.index(min(lengths))
        lengths[insert] = lengths[insert] + 3 + len(new_df.index)
        dfs[insert].append(new_df)

    row_datas = [[list(d.values.tolist()) for d in df] for df in dfs]

    return render_template('main.html', row_datas=row_datas, column_names=df.columns.tolist(),
                           link_column="image", zip=zip, city=city)

app_server = gevent.pywsgi.WSGIServer(('0.0.0.0', int(os.environ.get("PORT", 5000))), app)
app_server.serve_forever()