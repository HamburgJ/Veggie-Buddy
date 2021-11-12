import pandas as pd
from nltk.stem import WordNetLemmatizer
import nltk
from constants import *
from functions import *
import threading

def run_get_data(store, postal_code, city, start):
    results.append(get_data(store, postal_code, city, start))

if __name__ == "__main__":
    # Turn of pandas warnings
    pd.options.mode.chained_assignment = None
    
    results = []
    threads = []

    start = time.time()
    for city, postal_code in postal_codes.items():
        for store in websites:
            thread = threading.Thread(target=run_get_data, args=(store, postal_code, city, start,))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()
    print(len(results))
    #delete_items()
    nltk.download('wordnet')

    for df in results:
        process(df)

    print('Grocery data update complete!')
