import pandas as pd
import re
import ftfy
from nltk.stem import WordNetLemmatizer
import nltk
from requests_html import AsyncHTMLSession
category_map = pd.read_csv('category map.csv')

stores = ['Food Basics', 'FreshCo', "Metro", "Loblaws", "No Frills", "Giant Tiger", 'Walmart']
websites = {
    'Food Basics' : 'https://ecirculaire.foodbasics.ca/flyers/foodbasics-flyer/grid_view/661019',
    'FreshCo' : 'https://flyers.freshco.com/flyers/freshco-flyer/grid_view/656515',
    "Metro" :  'https://ecirculaire.metro.ca/flyers/metro-flyer/grid_view/663149',
    "Loblaws": 'https://flyers.loblaws.ca/flyers/loblaws-dryrun/grid_view/650023',
    "No Frills": 'https://flyers.nofrills.ca/flyers/nofrills-weeklyflyer/grid_view/650453',
    "Giant Tiger": 'https://eflyers.gianttiger.com/flyers/gianttiger-weeklyflyer/grid_view/650424',
    'Walmart': 'https://flyers.walmart.ca/flyers/walmartcanada-groceryflyer/grid_view/651584'
}
## keywords for sorting into brands and vegan
store_brands = ['selection', 'irresistibles', 'compliments', 'no name', 'pc', 'giant value', 'great value', 
                "president's choice", 'best buy', 'presidents choice', 'president choice', 
                'naturally imperfect', 'blue menu', 'your fresh market','carnaby sweet']
vegan_keywords = ['violife','daiya','gardein','silk','yves', 'just plant', 'plant egg', 'just egg', 'plant based', 'beefless', 'cheese-style', 'chickenless',
            'beyond meat', 'sol cuisine', 'earths own', 'blue diamond', 'boca', 'sunrise soya', 'fontaine', 'sunrise soft', 'lightlife',
            'field roast', 'so delicious', 'oat yeah', 'plant-based', 'vegan', 'vegetalien', 'tofu', 'wholly veggie', 'zoglos', 'tempeh',
            'almond milk', 'seitan', 'veggie ground', 'veggie meat', 'meat replacement', 'vegtable broth', 'hippie snacks',
            "chick'n", 'vio life', 'unmeatable', 'nut cheese', 'cashew cheese', 'cashew spread', 'big mountain',
            'tofurky', 'chao', 'sweets from the earth', 'earth island', 'cashew dip', 'zhoug', 'crabless', 'fishless', 'miyokos', "miyoko's",
            'miyoko', 'nuts for cheese', 'fauxmagerie', 'vegetarian', 'non-dairy', 'dairy free', 'larabar', 'clif',
            'nuts for butter', 'becel', 'beyond burger', 'beyond sausage', 'beyond chicken', 'beyound ground', 'beyond beef']

meat_keywords = ['salami', 'turkey', 'sardines','quiche', 'cheese', 'salmon', 'bacon', 'beef', 'chicken', 'ice cream', 'milk', 'yogurt', 'cream', 'egg', 'eggs',
                'danone', 'activia', 'butter', 'pizza', 'hungry-man', 'honey', 'rinds', 'cake', 'whites', 'fish',
                'yogourt', 'yoplait', 'fillets', 'steak', 'parlour', 'pogo', 'entrees', 'iögo', 'crema', 'nestlé pouches',
                "i can't believe it's not butter!", 'yop', 'chool whip', 'skyr', 'cheestrings', 'black diamond']
non_vegan = ['store made','mix and match deal','cheesecake', 'pizza', 'yoplait', 'minigo', 'yogurt', 'hungry-man', 'parmesan', 'baby', 'purée', 'cheez whiz', 'kraft dinner', 'canned tuna', 'online grocery']

foods = ['avocados', 'cilantro', 'broccoli', 'tomatoes', 'cantaloupes', 'cauliflower', 'potatoes', 'mandarins',
         'apples','cucumbers', 'cabbages', 'jalapeños', 'lemons',
         'blueberries', 'tangelos', 'grapefruits', 'raspberries', 'blackberries', 'strawberries', 'grapes', 
         'yams', 'dates', 'pineapples', 'peppers',
         'pears', 'celery', 'mangoes', 'watermelons', 'asparagus', 'bananas', 'peaches',
         'plums', 'limes', 'nectarines', 'frozen fruit', 'mushrooms',
         'carrots', 'ginger', 'garlic', 'radishes', 'spinach' ]

food_images = ['https://assets.shop.loblaws.ca/products/20142232001/b1/en/front/20142232001_front_a01_@2.png']

conditional=[ 'dairy','frozen','meat']

def hasword(string, positive, negative=[]):
    if negative != []:
        if (re.search('(?:(?<=\s)|(?<=^))('+ '|'.join(positive)+')(?=\s|$|,)', string)
            and not re.search('(?:(?<=\s)|(?<=^))('+ '|'.join(negative)+')(?=\s|$|,)', string)):
                return True
    else:
        if re.search('(?:(?<=\s)|(?<=^))('+ '|'.join(positive)+')(?=\s|$|,)', string):
            return True
    return False

async def get_data(store):
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

asession = AsyncHTMLSession()

results = asession.run(
    lambda: get_data('Food Basics'),
    lambda: get_data('FreshCo'),
    lambda: get_data('Metro'), 
    lambda: get_data('Loblaws'),
    lambda: get_data('No Frills'),
    lambda: get_data('Giant Tiger'),
    lambda: get_data('Walmart'),
)
nltk.download('wordnet')
df = pd.concat(results)

# preprocessing
df['category'] = df['category'].str[9:]
df['name'] = [ftfy.fix_text(str(x).lower()).replace("®","").replace('mangos', "mangoes").replace("sweet potatoes", "yams").replace("jalapeño pepper", "jalepeno").replace('chili pepper','chili').replace('clementine', 'orange').replace('mandarin','orange').replace('salads','salad') for x in df['name']]
df['price'] = [ftfy.fix_text(str(x).lower()).replace("¢", "").replace('or less than 2', 'or').replace('or less than 3', 'or').replace('or less than 4', 'or').replace('or less than 5', 'or').replace('or less than 6', 'or').replace('less than 2', 'or').replace('less than 3', 'or').replace('less than 4', 'or').replace('less than 5', 'or').replace('less than 6', 'or').replace('each', 'ea.').replace(' ea.', "").replace(' or /lb', "").replace('/lb', 'lb').replace(" .", " $0.").replace(' ea', '').replace(" for", "/").replace(' ealb', '').replace('lb.','lb') for x in df['price']]
df['story'] = [ftfy.fix_text(str(x).lower()) for x in df['story']]
df.dropna(subset=['price', 'story'], inplace=True)

# reformat consistant categories
group1s = []
group2s = []
cats = list(category_map['category'])
for category in df['category']:
    if category not in cats:
        group1s.append('delete')
        group2s.append('delete')
    else:
        line = category_map[category_map['category'] == category].index[0]
        group1s.append(category_map['group2'][line])
        group2s.append(category_map['group1'][line])

df['category'] = group1s
df['category 2'] = group2s
df = df[df['category'] != 'delete']

df.reset_index(inplace=True,drop=True)
df.drop_duplicates(inplace=True, subset=['name','price','store'])
df.reset_index(inplace=True,drop=True)


# detect brand names and vegan keywords
df['storebrands'] = ["FALSE" for x in range(0, len(df.index))]
df['vegan'] = ["FALSE" for x in range(0, len(df.index))]

for i in range(len(df.index)-1):
    for keyword in meat_keywords:
        if re.search('(?:(?<=\s)|(?<=^))'+keyword+'(?=\s|$|,)', df['name'][i]):
            df['category 2'][i] = 'meat'

    for keyword in vegan_keywords:
        if re.search('(?:(?<=\s)|(?<=^))'+keyword+'(?=\s|$|,)', df['name'][i]):
            df['category 2'][i] = 'vegan'


# detect size information
df['size'] = ["" for x in range(0, len(df.index))]

for i in range(0, len(df.index)):
    size = re.search("(?:(?<=\s)|(?<=^)?)(?:[,]?)(?:(?<=\s)|(?<=^))(?:[0-9-]+)\s?(?:mg|g|kg|ml|l|oz|lb|lbs|\"|inch|cm)(?=\s|$)", str(df['name'][i]))
    try:
        size.group(1)
    except IndexError:
        sizename = str(size.group(0))
        df['size'][i] = sizename
    except AttributeError:
        pass

# get price info
prices = [0 for x in range(len(df.index))]
for i in range(0, len(df.index)):
    string = df['price'][i]
    deal = re.search("([0-9])\s?(?:\/|for)\s\$([0-9]+.[0-9][0-9])", string)
    if deal:
        prices[i] = float(deal.group(2))/float(deal.group(1))
    else:
        p = re.search("\$([0-9]+.[0-9][0-9])", string)
        if string.find('lb')>-1:
            prices[i] = 100000
        if p:
            prices[i] = prices[i] + float(p.group(1))
        else:
            prices[i] = 10000000000
df['real price'] = prices 

df['foods'] = [[] for x in range(0, len(df.index))]
df['food categories'] = [[] for x in range(0, len(df.index))]

lemmatizer = WordNetLemmatizer()
# detect food items
for i in range(0, len(df.index)):
    name = df['name'][i]
    if (df['category 2'][i] == "produce") or (df['store'][i] in ['Food Basics','Giant Tiger'] and df['category 2'][i] == 'none'):
        for food in foods:
            if (re.search('(?:(?<=\s)|(?<=^))'+food+'(?=\s|$|,)', name) or
                re.search('(?:(?<=\s)|(?<=^))'+lemmatizer.lemmatize(food)+'(?=\s|$|,)', name) or
                re.search('(?:(?<=\s)|(?<=^))'+food+'(?=\s|$|,)', lemmatizer.lemmatize(name))):
                df['foods'][i].append(food)
                df['food categories'][i].append('produce')
    
    #becel
    if hasword(name, ['becel']):
        df['foods'][i].append('becel')
        df['food categories'][i].append('vegan')
    #coffee
    if hasword(name, ['coffee','roast and ground','maxwell house','nabob bag']):
        df['foods'][i].append('coffee')
        df['food categories'][i].append('other')
    #milk
    if hasword(name, ['coconut dream','silk','blue diamond','almond milk','oat yeah','soy milk','soy beverage','almond beverage','oat beverage']):
        df['foods'][i].append('nut milk')
        df['food categories'][i].append('vegan')
    #coke
    if hasword(name, ['coke','pepsi','cola','soft drink','soda'], ['soda water']):
        df['foods'][i].append('cola')
        df['food categories'][i].append('other')
    #chips
    if hasword(name, ['chips','smartfood','cheetos','bugels','doritos','lays','corn chips'], ['chocolate chips','carob chips']):
        df['foods'][i].append('chips')
        df['food categories'][i].append('other')
    #popcorn
    if hasword(name, ['popcorn', 'smartfood', 'bad monkey']):
        df['foods'][i].append('popcorn')
        df['food categories'][i].append('other')
    #crackers
    if hasword(name, ['crackers', 'triscuit','wheat thins','crispers','ritz','saltine','saltines']):
        df['foods'][i].append('crackers')
        df['food categories'][i].append('other')
    
    if hasword(name, ['cereal', 'cereals', 'general mills','shreddies','post'],['oatmeal']):
        df['foods'][i].append('cereal')
        df['food categories'][i].append('other')

    if hasword(name, ['oatmeal', 'oats'], ['of oats']):
        df['foods'][i].append('oats')
        df['food categories'][i].append('other')
    
    if hasword(name, ['chocolate', 'chocolates'], ['chocolate milk', 'chocolate ice','chocolate cream','chocolate pastry']):
        df['foods'][i].append('chocolate')
        df['food categories'][i].append('other')
    
    if hasword(name, ['dressing', 'dressings']):
        df['foods'][i].append('salad dressing')
        df['food categories'][i].append('other')

    if hasword(name, ['salad', 'salads'], ['dressing', 'dressings', 'fruit salad']):
        df['foods'][i].append('salad')
        df['food categories'][i].append('produce')
    
    if hasword(name, ['corn'], ['beef', 'chip', 'tortilla', 'chips', 'tortillas', 'popping']):
        df['foods'][i].append('corn')
        df['food categories'][i].append('produce')

    if hasword(name, ['onion', 'onions'], ['green onion', 'green onions', 'red onion', 'red onions']):
        df['foods'][i].append('onion')
        df['food categories'][i].append('produce')
    elif hasword(name, ['green onion', 'green onions']):
        df['foods'][i].append('green onion')
        df['food categories'][i].append('produce')
    elif hasword(name, ['red onion', 'red onions']):
        df['foods'][i].append('red onion')
        df['food categories'][i].append('produce')

    if hasword(name, ['green bean', 'green beans', 'long beans', 'fresh beans', 'french beans'], ['canned', 'pickled']):
        df['foods'][i].append('green beans')
        df['food categories'][i].append('produce')

    if hasword(name, ['romaine', 'lettuce'], ['salad', 'wrap']):
        df['foods'][i].append('lettuce')
        df['food categories'][i].append('produce')

    if hasword(name, ['yams', 'sweet potato', 'yam', 'sweet potato'], ['sauce', 'food', 'pie']):
        df['foods'][i].append('sweet potato')
        df['food categories'][i].append('produce')
    
    if hasword(name, ['classico', 'pasta sauce', 'prima', 'pasta sauces', 'marinara sauce', 'tomato sauce']):
        df['foods'][i].append('pasta sauce')
        df['food categories'][i].append('other')

    if hasword(name, ['fruit bowls','dole fruit']):
        df['foods'][i].append('fruit snack')
        df['food categories'][i].append('other')
    
    if hasword(name, ['peanut butter']):
        df['foods'][i].append('peanut butter')
        df['food categories'][i].append('other')

    if hasword(name, ['jam', 'jelly'], ['jellies']):
        df['foods'][i].append('jam')
        df['food categories'][i].append('other')

    if hasword(name, ['ketchup'], ['chips']):
        df['foods'][i].append('ketchup')
        df['food categories'][i].append('other')
    
    if hasword(name, ['mustard']):
        df['foods'][i].append('mustard')
        df['food categories'][i].append('other')
    
    if hasword(name, ['vinegar'], ['salt and', 'chips', 'crisps', 'fish', '']):
        df['foods'][i].append('vinegar')
        df['food categories'][i].append('other')
    
    if hasword(name, ['white sugar', 'brown sugar', 'icing sugar']):
        df['foods'][i].append('sugar')
        df['food categories'][i].append('other')

    if hasword(name, ['sparkling water', 'flavoured water', 'stevia water', 'fizzy water', 'bubly', 'montelliar', 'free and clear', 'carbonated water']):
        df['foods'][i].append('sparkling water')
        df['food categories'][i].append('other')

    if hasword(name, ['bagel', 'bagels'], ['hummus', 'bagel bite', 'bagel bites', 'mini', 'seasoning']):
        df['foods'][i].append('bagels')
        df['food categories'][i].append('bakery')

    if hasword(name, ['english muffins', 'english muffin'], ['maple', 'cinnamon']):
        df['foods'][i].append('english muffins')
        df['food categories'][i].append('bakery')
    
    if hasword(name, ['bread', 'loaf'], ['baguette', 'buns', 'bowl']):
        df['foods'][i].append('bread')
        df['food categories'][i].append('bakery')
    
    if hasword(name, ['tortilla', 'torillas'], ['chips','seasoning', 'hard', 'fried']):
        df['foods'][i].append('tortillas')
        df['food categories'][i].append('bakery')
    
    if hasword(name, ['hummus']):
        df['foods'][i].append('hummus')
        df['food categories'][i].append('vegan')
    
    if hasword(name, ['mixed nuts', 'nut mix', 'premium nuts', 'deluxe nuts']):
        df['foods'][i].append('mixed nuts')
        df['food categories'][i].append('other')

    if hasword(name, ['cookies', 'cookie', 'oreo', 'chips ahoy', 'voortman']):
        df['foods'][i].append('cookies')
        df['food categories'][i].append('bakery')
    
    if hasword(name, ['olive oil', 'canola oil', 'corn oil', 'vegetable oil', 'seed oil'], ['hummus', 'chips', 'olives', 'tomatoes']):
        df['foods'][i].append('oil')
        df['food categories'][i].append('other')

    if hasword(name, ['broth']):
        df['foods'][i].append('broth')
        df['food categories'][i].append('other')
    
    if hasword(name, ['pickles', 'gherkins'], ['chips', 'flavour']):
        df['foods'][i].append('pickles')
        df['food categories'][i].append('other')
    
    if hasword(name, ['buns']):
        df['foods'][i].append('buns')
        df['food categories'][i].append('bakery')

    if hasword(name, ['canned tomato', 'canned tomatoes', 'rotel', 'tomato paste', 'crushed tomato']):
        df['foods'][i].append('canned tomato')
        df['food categories'][i].append('other')
    
    if hasword(name, ['salsa']):
        df['foods'][i].append('salsa')
        df['food categories'][i].append('other')
    
    if hasword(name, ['tofu'], ['dip']):
        df['foods'][i].append('tofu')
        df['food categories'][i].append('vegan')
    
    if hasword(name, ['waffles', 'waffle'], ['beglian']):
        df['foods'][i].append('waffles')
        df['food categories'][i].append('other')

    if hasword(name, ['orange', 'oranges'], ['segments', 'canned', 'syrup', 'candy', 'popcicles', 'chicken', 'sauce', 'juice', 'pekoe', 'drink', 'tropicana', 'soda', 'pop', 'sodas', 'sparkling', 'cookie', 'cookies', 'pulp', 'pure', 'marmalade', 'water','fanta', 'tic tac', 'zevia', 'gatorade', 'peel', 'crush', 'jelly', 'jam', 'jello', 'powder', 'crystals', 'tang', 'bar', 'soap', 'shampoo', 'chocolate']):
        df['foods'][i].append('oranges')
        df['food categories'][i].append('produce')
    

for i in range(0, len(df.index)):
    if df['foods'][i] == []:
        df['foods'][i] = [df['name'][i]]
        df['food categories'][i] = [df['category 2'][i]]

rows = []
row_food_labels = []
category_labels = []
for i in range(0, len(df.index)):
    for j in range(len(df['foods'][i])):
        rows.append(df.iloc[i])
        row_food_labels.append(df['foods'][i][j])
        category_labels.append(df['food categories'][i][j])

final_df = pd.DataFrame(rows, columns=['name','price','store','image','story','storebrands','vegan','size','foods', 'real price'])
final_df['name'] = [x.capitalize() for x in final_df['name']]
final_df.insert(loc=0, column="category", value=category_labels)
final_df.insert(loc=0, column="item", value=row_food_labels)
final_df.sort_values(inplace=True, by=['real price'])
final_df.reset_index(drop=True,inplace=True)

# fix image to be of item with fewest foods found
for i in range(0,len(row_food_labels)):
    item_df = pd.DataFrame(final_df.loc[final_df['item'] == row_food_labels[i]], columns = ['foods','image'])
    item_df.reset_index(inplace=True, drop=True)
    if len(item_df) > 1:
        shortest = 0
        for j in range(0, len(item_df)):   
            if (len(item_df['foods'][j]) < len(item_df['foods'][shortest])):
                shortest = j
        final_df.loc[final_df['item'] == row_food_labels[i], 'image'] = item_df['image'][shortest]

# Saving to MongoDB

from pymongo import MongoClient

# Connect to MongoDB
client =  MongoClient("mongodb+srv://joshi:joshi@cluster0.fns0o.mongodb.net/groceryDatabase?retryWrites=true&w=majority")
db = client['groceryDatabase']
collection = db['groceryCollection']
data_dict = final_df.to_dict("records")

# Reset and Insert collection
collection.delete_many({})
collection.insert_many(data_dict)
print('done?')
