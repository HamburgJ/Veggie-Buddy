import pandas as pd
from nltk.stem import WordNetLemmatizer
import nltk
from constants import *
from functions import *
import threading

if __name__ == "__main__":
    # Turn of pandas warnings
    pd.options.mode.chained_assignment = None

    global results
    results = []
    threads = []

    start = time.time()
    for city, postal_code in postal_codes.items():
        for store in websites:
            thread = threading.Thread(target=get_data, args=(store, postal_code, city, start,))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    delete_items()
    nltk.download('wordnet')

    for df in results:
        process(df)

    print('Grocery data update complete!')
