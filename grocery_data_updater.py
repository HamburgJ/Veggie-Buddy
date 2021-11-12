import pandas as pd
from nltk.stem import WordNetLemmatizer
import nltk
from requests_html import AsyncHTMLSession
from constants import *
from functions import *

# Turn of pandas warnings
pd.options.mode.chained_assignment = None

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

#delete_items()
nltk.download('wordnet')

for data in r:
    results.append(data)

for df in results:
    process(df)

print('Grocery data update complete!')
