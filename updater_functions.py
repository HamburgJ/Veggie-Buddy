import re
from constants import *
import pandas as pd
import time
from requests_html import AsyncHTMLSession

# Checks if any of the postitive words are in the string and none of the negative are
def hasword(string, positive, negative=[]):
    if negative != []:
        if (re.search('(?:(?<=\s)|(?<=^))('+ '|'.join(positive)+')(?=\s|$|,)', string)
            and not re.search('(?:(?<=\s)|(?<=^))('+ '|'.join(negative)+')(?=\s|$|,)', string)):
                return True
    else:
        if re.search('(?:(?<=\s)|(?<=^))('+ '|'.join(positive)+')(?=\s|$|,)', string):
            return True
    return False

# Processing website item data to dataframe
async def get_data(store, postal_code, city):
    if store != 'Farmboy':
        params = {
            'postal_code': postal_code,
            'locale' : 'en',
            'type' : 1
        }
    else:
        params = {}
    #print('getting a data')
    start = time.time()
    r = await AsyncHTMLSession().get(websites[store], params=params)
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

    #print('done. time took: {} link: {} postal: {}'.format(time.time() - start, websites[store], postal_code))

    if len(rows) > 0:
        store_data = pd.concat(rows)
        return store_data

    return pd.DataFrame()