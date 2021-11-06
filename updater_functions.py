import re
from constants import *
import pandas as pd

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
async def get_data(store, asession):
    r = await asession.get(websites[store], params = { 'postal_code' : 'M5R2A7', 'locale' : 'en', 'type' : 1})
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

        rows.append(pd.DataFrame({'name' : names,
                                 'price' : prices,
                                 'store': this_stores,
                                 'image' : imgs,
                                 'story' : stories,
                                 'category': categories}))
        category = category + 1

    store_data = pd.concat(rows)
    return store_data