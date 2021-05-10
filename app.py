from flask import Flask, render_template, request, send_file, url_for
import pandas as pd
import random
import os
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Connect to MongoDB
    client =  MongoClient("mongodb+srv://joshi:joshi@cluster0.fns0o.mongodb.net/groceryDatabase?retryWrites=true&w=majority")
    db = client['groceryDatabase']
    collection = db['groceryCollection']
    df = pd.DataFrame(list(collection.find()))

    df['story'] = [ str(x).replace("nan", "") for x in df['story']]
    df['price'] = [ str(x).replace("nan", "") for x in df['price']]

    # reformat data to list of dfs
    items = list(set(df['item']))
    colnum = 5
    dfs = [[] for x in range(colnum)]
    lengths = [0 for x in range(colnum)]
    categories = [[] for x in range(len(items))]
    for i in range(0,len(items)):
        new_df = pd.DataFrame(df.loc[df['item'] == items[i]], columns=['item','name','price','store','image','story','category','storebrands','vegan','size','foods'])
        if len(new_df.index)>2:
            new_df['hiddenresult']=['FALSE' if x<2 else 'TRUE' for x in range(0,len(new_df.index-2))]

        insert = lengths.index(min(lengths))
        lengths[insert] = lengths[insert] + 3 + len(new_df.index)
        dfs[insert].append(new_df)

    row_datas = [[list(d.values.tolist()) for d in df] for df in dfs]

    phrase = "veggie buddy"

    return render_template('main.html', row_datas=row_datas, column_names=df.columns.tolist(),
                           link_column="image", zip=zip, phrase=phrase)

app_server = gevent.pywsgi.WSGIServer(('0.0.0.0', int(os.environ.get("PORT", 5000))), app)
app_server.serve_forever()