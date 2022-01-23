import pandas as pd
from settings import *
import math

def clean_text(txt_in):
    import re
    clean = re.sub('[^a-zA-Z0-9]+', " ", txt_in).strip() 
    # Normally should lowercase the text, but for the object of counting the frequency of ticker,
    # and the fact that the ticker names are written in Uppercase, no need to lower case.
    return clean

data_path='C:/Users/hs324/OneDrive/Desktop/Class_Files/GR5067_NLP/03_Group_Project/'
ticker = pd.read_csv(data_path + 'ticker.csv')
ticker = ticker['symbol'].to_list()
# Discard the words that formats in uppercase but not being the ticker.
ticker = [x for x in ticker if x not in blacklist] #4787

def uppers_fun(string):
    tmp_txt = [word for word in string.split() if word in ticker]
    return tmp_txt

def tokenizer(txt):
    return txt.split()

def joiner(txt):
    txt = ' '.join(txt)
    return txt

def counter(txt):
    return pd.DataFrame(txt).value_counts()

def percentile(data, perc: int):
    size = len(data)
    return sorted(data)[int(math.ceil((size * perc) / 100)) - 1]

def rem_sw(var):
    from nltk.corpus import stopwords
    sw = set(stopwords.words("English"))
    my_test = [word for word in var.split() if word not in sw]
    my_test = ' '.join(my_test)
    return my_test

def stem_fun(var):
    from nltk.stem.porter import PorterStemmer
    stemmer = PorterStemmer()
    tmp_txt = [stemmer.stem(word) for word in var.split()]
    tmp_txt = ' '.join(tmp_txt)
    return tmp_txt