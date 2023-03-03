from requests import get
from bs4 import BeautifulSoup
import pandas as pd

import re
import os
import json
import unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.tokenize.toktok import ToktokTokenizer
from time import strftime

import pymysql

import matplotlib.pyplot as plt
import seaborn as sns

from wordcloud import WordCloud

#--------------------------------------------------------------------





def clean_text(text, extra_stopwords=['r', 'u', '2', 'ltgt']):
    '''
    This function does what 'basic_clean' does, but takes it a step further by removing stopwords and lemmatizing the text.
    '''
    wnl = nltk.stem.WordNetLemmatizer()
    
    stopwords = nltk.corpus.stopwords.words('english') + extra_stopwords
    
    clean_text = (unicodedata.normalize('NFKD', text)
                   .encode('ascii', 'ignore')
                   .decode('utf-8', 'ignore')
                   .lower())
    
    words = re.sub(r'[^\w\s]', '', clean_text).split()
    
    return [wnl.lemmatize(word) for word in words if word not in stopwords]

#--------------------------------------------------------------------

def tokenize(string):
    '''
    This function takes in a string and returns the string as individual tokens put back into the string
    '''
    #create the tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()

    #use the tokenizer
    string = tokenizer.tokenize(string, return_str = True)

    return string

#--------------------------------------------------------------------

def stem(string):
    '''
    This function takes in text and returns the stem word joined back into the text
    '''
    #create porter stemmer
    ps = nltk.porter.PorterStemmer()
    
    #use the stem, split string using each word
    stems = [ps.stem(word) for word in string.split()]
    
    #join stem word to string
    string = ' '.join(stems)

    return string

#--------------------------------------------------------------------

def lemmatize(string):
    '''
    This function takes in a string and returns the lemmatized word joined back into the string
    '''
    #create the lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    
    #look at the article 
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    
    #join lemmatized words into article
    string = ' '.join(lemmas)

    return string


#--------------------------------------------------------------------

def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    This function takes in text, extra words and exclude words
    and returns a list of text with stopword removed
    '''
    #create stopword list
    stopword_list = stopwords.words('english')
    
    #remove excluded words from list
    stopword_list = set(stopword_list) - set(exclude_words)
    
    #add the extra words to the list
    stopword_list = stopword_list.union(set(extra_words))
    
    #split the string into different words
    words = string.split()
    
    #create a list of words that are not in the list
    filtered_words = [word for word in words if word not in stopword_list]
    
    #join the words that are not stopwords (filtered words) back into the string
    string = ' '.join(filtered_words)
    
    return string

#--------------------------------------------------------------------

def word_cloud(words):
    '''
    This function will simply create word cloud, given a series of words.
    '''
    series = WordCloud(background_color='white').generate(' '.join(words))
    plt.figure(figsize=(12, 8))
    plt.imshow(series)
    plt.axis('off')
    plt.show()

#--------------------------------------------------------------------

def basic_clean(words):
    
    words = unicodedata.normalize('NFKD', words)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    
    words = re.sub(r"[^\w0-9'\s]", '', words).lower()
    return words

def tokenize(words):
    
    tokenize = nltk.tokenize.ToktokTokenizer()
    
    words = tokenize.tokenize(words, return_str = True)
    
    return words

def stem(words):
    
    ps = nltk.porter.PorterStemmer()
    
    stemmed_words = [ps.stem(word) for word in words.split()]
    
    new_text = ' '.join(stemmed_words)
    
    return new_text

def lemmatize(words):
    
    wnl = nltk.stem.WordNetLemmatizer()
    
    lemmas = [wnl.lemmatize(word) for word in words.split()]
    
    new_text = ' '.join(lemmas)
    
    return new_text

def remove_stopwords(x, extra_words = [], exclude_words = []):

    stopword_list = stopwords.words('english')

    stopword_list = set(stopword_list) - set(exclude_words)

    stopword_list = stopword_list.union(set(extra_words))

    words = x.split()

    filtered_words = [word for word in words if word not in stopword_list]

    string_without_stopwords = ' '.join(filtered_words)

    return string_without_stopwords


def prep_article_data(df, column, extra_words=[], exclude_words=[]):

    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords,
                                  extra_words=extra_words,
                                  exclude_words=exclude_words)
    
    df['stemmed'] = df['clean'].apply(stem)
    
    df['lemmatized'] = df['clean'].apply(lemmatize)
    
    return df[['title', column,'clean', 'stemmed', 'lemmatized']]

#--------------------------------------------------------------------



#--------------------------------------------------------------------



#--------------------------------------------------------------------