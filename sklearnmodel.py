###using tensorflow
### 8/15/2024

#### import all Necessary Libraries # ##################

from textblob import TextBlob
import nltk
from nltk.stem import PorterStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


dtree_model = ""
vectorizer2 = TfidfVectorizer(stop_words='english', max_features=1)
ps=PorterStemmer()
trained = False

def trainmodel():
    global vectorizer2
    global dtree_model
    global ps
    global trained

    if(trained == False):
       #Grabbing the data from the file
        hotel_dataset = pd.read_csv("./static/trainingdata.csv")

        # Feature Extraction: Use NLP techniques like tokenization, stemming, and vectorization with libraries like spaCy or NLTK.

        x_nlp = []
        
        # looping through the review's
        for review in hotel_dataset['Review']:
            blob = TextBlob(review)
            blob_words = blob.words
            stemmedwords = []
            for w in blob_words:
                stemmedwords.append(ps.stem(w))
            # rebuilding the string
            rebuilt_stemmed_words = ' '.join(stemmedwords)
            x_nlp.append(rebuilt_stemmed_words)


        # item_number = 7
        # print(x_nlp[item_number])
        # print(hotel_dataset['Label'][item_number])
        hotel_dataset['Review'] = x_nlp

        # Now we will fit the data to the model
        
        # Initialize TF-IDF Vectorizer
        


        # currently not working
        # the data has been splitt properly
        x = vectorizer2.fit_transform(hotel_dataset['Review'])
        y = hotel_dataset['Label']

        # x_test = vectorizer.fit_transform(testset['Review'])
        # y_test = testset['Label']

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=65)

        #going to start with creating the model then I will impliment the feature extraction

        from sklearn.tree import DecisionTreeClassifier 
        from sklearn.metrics import confusion_matrix 


        dtree_model = DecisionTreeClassifier(max_depth = 2).fit(x_train, y_train) 
        dtree_predictions = dtree_model.predict(x_test) 
        
        # creating a confusion matrix 
        cm = confusion_matrix(y_test, dtree_predictions) 
        print(cm)
        accuracy = accuracy_score(y_test, dtree_predictions)
        report = classification_report(y_test, dtree_predictions, target_names = ['Positive', 'Neutral', 'Negative'] )

        print('The accuracy is : ', accuracy)
        print(report)
        trained = True
    
    
    


def run_sk_model(input_string):
    global dtree_model
    global vectorizer2
    global ps
    #stemming the input string
    blob = TextBlob(input_string)
    blob_words = blob.words
    stemmedwords = []
    for w in blob_words:
        stemmedwords.append(ps.stem(w))
        # rebuilding the string
    rebuilt_stemmed_words = ' '.join(stemmedwords)

    stemmed_blob = TextBlob(rebuilt_stemmed_words)
    input_arr = []
    for s in stemmed_blob.sentences:
        input_arr.append(str(s))

    vectorized_input_string = vectorizer2.fit_transform(input_arr)
    print(input_arr)
    prediction = dtree_model.predict(vectorized_input_string)
    print(prediction)
    prediction_arr = ["Positive", "Neutral", "Negative"]
    
    return prediction_arr[prediction[0]]

