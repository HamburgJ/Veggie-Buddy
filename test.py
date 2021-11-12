from lxml import html  
import csv,os,json
import requests
import time
from constants import *
import pandas as pd
url="https://flyers.sobeys.com/flyers/sobeys-flyer/grid_view/656515"
r=requests.get(url)
t=html.fromstring(r.content)

def get_data_new(store, postal_code, city):
    params = {
        'postal_code': postal_code,
        'locale' : 'en',
        'type' : 1
    }

    start = time.time()

    path = '//*[@id="wrapper"]/div[8]/div/div[2]/div['
    try:
        
        r = requests.get(websites[store], params=params)
        r_html = html.fromstring(r.content)

        category = 2
        rows = []
        
        while len(r_html.xpath('{}{}]/text()'.format(path, category))) != 0:

            category_name = r_html.xpath('{}{}]'.format(path, category))[0].get('class')

            imgs = r_html.xpath('{}{}]/ul/li/div[1]/div/a/img/@src'.format(path, category))
            prices = r_html.xpath('{}{}]/ul/li/div[3]/text()'.format(path, category))
            stories = [x.replace('nan', "") for x in r_html.xpath('{}{}]/ul/li/div[2]/text()'.format(path, category))]
            names = r_html.xpath('{}{}]/ul/li/div[4]/text()'.format(path, category))
            
            entries = len(imgs)
            
            this_stores = [store for x in range(entries)]
            categories = [category_name for x in range(entries)]
            this_locations = [city for x in range(entries)]

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