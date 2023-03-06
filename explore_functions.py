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

def word_count():
    '''this function takes in teh word counts of our dataframe and produces
    the highest counted words by language into a bar plot
    '''
    word_freq.sort_values('all', ascending=False).head(5).plot.bar(figsize=(16, 9))
    plt.title('Most common words by category')
    plt.ylabel('Count')
    plt.xlabel('Most common words')
    plt.xticks(rotation=45)
    plt.show()

#---------------------------------------------------------------

def clean_df(df):
    
    df = df.drop([29, 139])

    df = df.dropna()

    others = ['TypeScript', 'Jupyter Notebook', 'Java', 'C#', 'Swift', 'CSS', 'C', 'C++', 'Kotlin',
         'VimL', 'Handlebars', 'Vue', 'Go', 'SCSS', 'Emacs Lisp', 'Vim Script', 'Lua', 'TeX',
         'Rust', 'Shell', 'PHP', 'Vim script', 'CoffeeScript']

    df = df.replace(to_replace=others, value="Other")

    df['language'] = df['language'].str.lower()
    
    return df

#---------------------------------------------------------------

def word_counts(df):
    
    other_words = prep.clean_text(' '.join(df[df['language'] == 'Other']['readme_contents']))
    javascript_words = prep.clean_text(' '.join(df[df['language'] == 'JavaScript']['readme_contents']))
    html_words = prep.clean_text(' '.join(df[df['language'] == 'HTML']['readme_contents']))
    dart_words = prep.clean_text(' '.join(df[df['language'] == 'Dart']['readme_contents']))
    ruby_words = prep.clean_text(' '.join(df[df['language'] == 'Ruby']['readme_contents']))
    python_words = prep.clean_text(' '.join(df[df['language'] == 'Python']['readme_contents']))
    all_words = prep.clean_text(' '.join(df['readme_contents']))

    other_counts = pd.Series(other_words).value_counts()
    javascript_counts = pd.Series(javascript_words).value_counts()
    html_counts = pd.Series(html_words).value_counts()
    dart_counts = pd.Series(dart_words).value_counts()
    ruby_counts = pd.Series(ruby_words).value_counts()
    python_counts = pd.Series(python_words).value_counts()
    all_counts = pd.Series(all_words).value_counts()

    
    word_freq = pd.concat([other_counts, javascript_counts, html_counts, dart_counts, 
                       ruby_counts, python_counts, all_counts], axis=1)

    word_freq.fillna(0, inplace=True)
    
    word_freq = word_freq.astype('int')

    word_freq = word_freq.rename(columns={0:'other', 1:'javascript', 2:'html', 3: 'dart', 4:'ruby', 5:'python', 6:'all_counts'})

    return word_freq