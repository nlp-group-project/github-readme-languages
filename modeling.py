from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, plot_confusion_matrix, recall_score

#-----------------------------------------------------

def random_forest(X_train, y_train, X_validate, y_validate):
    '''
    This function will, given x/y train and validate sets, create a random forest model on the data and return the train and validate accuracies.
    '''
    results = []
    # creating and transforming x train with the lemmatized data on a random forest model
    X_bow = cv.fit_transform(X_train)
    tree = RandomForestClassifier(max_depth=6, 
                            min_samples_leaf=3,
                            n_estimators=100, 
                            random_state=42, )

    # fitting the data and getting the accuracy score 
    tree.fit(X_bow, y_train)
    train = tree.score(X_bow, y_train)
    results.append(train)
    
    # transforming and getting the validate accuracy on the model
    X_val_bow = cv.transform(X_validate)
    validate = tree.score(X_val_bow, y_validate)
    results.append(validate)
    
    print(f'Train Accuracy:    {train:.4}')
    print(f'Validate Accuracy: {validate:.4}')

#-----------------------------------------------------

def dec_tree(X_train, y_train, X_validate, y_validate):
    '''
    This function will, given x/y train and validate sets, create a decision model on the data and return the train and validate accuracies.
    '''
    results = []
    # creating and transforming x train with the lemmatized data on a random forest model
    X_bow = cv.fit_transform(X_train)
    dec = DecisionTreeClassifier(max_depth=3, random_state=42)

    # fitting the data and getting the accuracy score 
    dec.fit(X_bow, y_train)
    train = dec.score(X_bow, y_train)
    results.append(train)
    
    # transforming and getting the validate accuracy on the model
    X_val_bow = cv.transform(X_validate)
    validate = dec.score(X_val_bow, y_validate)
    results.append(validate)
    
    print(f'Train Accuracy:    {train:.4}')
    print(f'Validate Accuracy: {validate:.4}')

#-----------------------------------------------------

def knn(X_train, y_train, X_validate, y_validate):
    '''
    This function will, given x/y train and validate sets, create a knn model on the data and return the train and validate accuracies.
    '''
    results = []
    # creating and transforming x train with the lemmatized data on a random forest model
    X_bow = cv.fit_transform(X_train)
    knn = KNeighborsClassifier(n_neighbors=5, weights='uniform')

    # fitting the data and getting the accuracy score 
    knn.fit(X_bow, y_train)
    train = knn.score(X_bow, y_train)
    results.append(train)
    
    # transforming and getting the validate accuracy on the model
    X_val_bow = cv.transform(X_validate)
    validate = knn.score(X_val_bow, y_validate)
    results.append(validate)
    
    print(f'Train Accuracy:    {train:.4}')
    print(f'Validate Accuracy: {validate:.4}')

#-----------------------------------------------------

def dec_test_accuracy(X_train, y_train, X_validate, y_validate, X_test, y_test):
    '''
    This function will, given x/y train, validate, and test sets, create a decision tree model on the data and return the train, validate, and test accuracies. Made to reproduce best model results.
    '''
    results = []
    # creating and transforming x train with the lemmatized data on a random forest model
    X_bow = cv.fit_transform(X_train)
    dec = DecisionTreeClassifier(max_depth=3, random_state=42)

    # fitting the data and getting the accuracy score 
    dec.fit(X_bow, y_train)
    train = dec.score(X_bow, y_train)
    results.append(train)
    
    # transforming and getting the validate accuracy on the model
    X_val_bow = cv.transform(X_validate)
    validate = dec.score(X_val_bow, y_validate)
    results.append(validate)
    
    X_val_bow = cv.transform(X_test)
    test = dec.score(X_val_bow, y_test)
    results.append(test)
    
    print(f'Train Accuracy:    {train:.4}')
    print(f'Validate Accuracy: {validate:.4}')
    print(f'Test Accuracy:     {test:.4}')

#-----------------------------------------------------



#-----------------------------------------------------