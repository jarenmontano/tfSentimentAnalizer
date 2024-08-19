###using tensorflow
### 8/15/2024

#### import all Necessary Libraries # ##################

from textblob import TextBlob
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import pandas as pd
from sklearn.model_selection import train_test_split

model = ""
vectorizer = TfidfVectorizer(stop_words='english', max_features=1) 
ps=PorterStemmer()
trained = False
scores = ""


def trainingmodel():
    # setting global variables
    global vectorizer
    global model
    global ps
    global trained
    global scores

    if(trained == False):
    #Grabbing the data from the file
        hotel_dataset = pd.read_csv("./static/trainingdata.csv")

        # Feature Extraction: Use NLP techniques like tokenization, stemming, and vectorization with libraries like spaCy or NLTK.


        x_nlp = []
        ps=PorterStemmer()
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
        x = vectorizer.fit_transform(hotel_dataset['Review'])
        y = hotel_dataset['Label']

        # x_test = vectorizer.fit_transform(testset['Review'])
        # y_test = testset['Label']

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=65)


        #https://www.tensorflow.org/tutorials/keras/text_classification
        import tensorflow as tf

        from tensorflow.keras import layers
        from tensorflow.keras.losses import SparseCategoricalCrossentropy

        embedding_dim = 16
        max_features = 10000
        #creating the model
        model = tf.keras.Sequential([
        layers.Embedding(max_features, embedding_dim),
        layers.Dropout(0.2),
        layers.GlobalAveragePooling1D(),
        layers.Dropout(0.2),
        layers.Dense(3, activation='sigmoid')])

        #model.summary()

        #configure the model
        model.compile(loss=SparseCategoricalCrossentropy(from_logits = True),
                    optimizer='adam',
                    metrics=['accuracy', 'r2_score'])



        #Train the model
        epochs = 10
        history = model.fit(
            x_train,
            y_train,
            batch_size = 16,
            epochs=epochs,
            validation_data =(x_test, y_test))



        #evaluating the model
        loss, accuracy, r2 = model.evaluate(x_test, y_test)

        print("Loss: ", loss)
        print("Accuracy: ", accuracy)
        print("R^2 score: ", r2)

        scores = {
            "Loss" : loss,
            "Accuracy" : accuracy,
            "r2_score" : r2
        }
        trained = True


    return scores

def RunTfModel(input_string):
    # setting global variables
    global vectorizer
    global model
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

    #  I am failing to get vectorization to work
    # Need to vectorize : must be in array format
    pd_input = pd.array(input_arr)
    vectorized_input_string = vectorizer.fit_transform(input_arr)
    print(input_arr)
    prediction = model.predict(vectorized_input_string)
    prediction_string = f"\nPositive : {prediction[0][0]:.2%} \nNeutral : {prediction[0][1]:.2%} \nNegative : {prediction[0][1]:.2%}"
    print(prediction_string)
    return prediction_string





