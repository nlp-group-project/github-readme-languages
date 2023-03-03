import os
import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split

#---------------------------------------------------------------

def split_train_test(df, col):
    '''
    
    '''
    seed = 42
    train, val_test = train_test_split(df, train_size=.5, random_state=seed, stratify=df[col])
    validate, test = train_test_split(val_test, train_size=.6, random_state=seed, stratify=val_test[col])
    
    return train, validate, test

#---------------------------------------------------------------

def xy_train(train, validate, test, target):
    '''
    This function will separate each of my datasets (train, validate, and test) and split them further into my x and y sets for modeling. 
    '''
    seed = 42
    
    X_train = train.drop(columns=[target])
    y_train = train[target]

    X_validate = validate.drop(columns=[target])
    y_validate = validate[target]

    X_test = test.drop(columns=[target])
    y_test = test[target]
    
    return X_train, y_train, X_validate, y_validate, X_test, y_test

#---------------------------------------------------------------

def lesser_langs_list(df):
    
    '''
    this function takes in the dataframe of scraped
    github data, cleans, lemmatises & removes stopwords,
    isolates the language column into word counts, then
    turns that col into a separate DF, isolates out the 
    top 6 languages, and turns all the remaining languages
    into a list
    '''
    
    #returning all the words in language individually
    lang_words = clean_text(' '.join(df['language']))

    # setting the cleaned txt to Series and counting word frequency
    count = pd.Series(lang_words).value_counts()

    # amke into df
    lang_df = pd.DataFrame(count)

    # language counts, resetting & renaming index
    lang_df.columns = ['counts']
    lang_df = lang_df.reset_index()
    lang_df = lang_df.rename(columns = {'index':'language'})

    # all the languages that are not in the top 6
    langs = ['javascript', 'html', 'cs', 'ruby', 'python', 'typescript']
    other_langs = lang_df[~lang_df['language'].isin(langs)]

    # dropping 'counts col'
    other_langs = other_langs.drop(columns=['counts'])
    
    # turning df into a list
    other_langs = other_langs.values.tolist()
    
    return other_langs

#---------------------------------------------------------------

# most frequent words, label-coloured
def lang_freq_barchart():
    
    top_freq.plot.bar(figsize = (9,6), color = 'magenta')

    plt.title('Github shoe repository programming language word counts')

    # set xtick labels and properties
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7], 
               ['Javascript', 'HTML', 'CSS', 'Ruby', 'Python', 'Typescript', 'Dart', 'Java'],
                rotation = 25)

    plt.legend([],[])
    plt.yticks(np.arange(0, 21, 2))

    plt.ylabel('Count')
    plt.xlabel('Repository language frequency')

    plt.show()

#---------------------------------------------------------------



#---------------------------------------------------------------



#---------------------------------------------------------------