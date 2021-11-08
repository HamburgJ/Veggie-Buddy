from flask import Flask, render_template, request
from pymongo import MongoClient
import pandas as pd
import random
import gevent.pywsgi
import os
from static_data import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Get data from MongoDB
    '''
    client =  MongoClient(os.environ['MONGODB_URI'])
    db = client['groceryDatabase']
    collection = db['groceryCollection']

    location = request.args.get('location', default = 'kingston', type = str).lower()
    query = {'location': location}
    df = pd.DataFrame(list(collection.find(query)))
    '''
    df = pd.DataFrame(data)

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
                           link_column="image", zip=zip)

#app_server = gevent.pywsgi.WSGIServer(('0.0.0.0', int(os.environ.get("PORT", 5000))), app)
#app_server.serve_forever()