import os
import pickle
import numpy as np
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Embedding
from keras.layers import Dense, Embedding
from keras.layers import LSTM

import warnings
warnings.filterwarnings('ignore')


def findTheSentiment(li):
    try:
        f = open("word_to_id.pkl", "rb")
        word_to_id = pickle.load(f)
        f.close()
        print("Loaded the dictionary of words")
    except:
        import pickle
        from keras.datasets import imdb
        word_to_id = imdb.get_word_index()
        word_to_id = {key:(value+3) for key,value in word_to_id.items()}
        word_to_id["<PAD>"] = 0
        word_to_id["<START>"] = 1
        # id_to_word = {value:key for key,value ino_id.items()}
        f = open("word_to_id.pkl", "wb")
        pickle.dump(word_to_id, f)
        f.close()
        # print("Please download the dictionary file first, run the python file downloadDictionary.py")


    # load the model
    try:
        # reconstructed_model = keras.models.load_model("myTrainedModel.model")
        print(os.getcwd()+"this is the path")
        reconstructed_model = Sequential()
        reconstructed_model.add(Embedding(input_dim = 100000, output_dim = 128))
        reconstructed_model.add(LSTM(units=128))
        reconstructed_model.add(Dense(units=1, activation='sigmoid'))
        reconstructed_model.compile(loss='binary_crossentropy', optimizer = "RMSprop", metrics=['accuracy'])
        reconstructed_model.load_weights(os.getcwd()+"/weigts.h5")
        print("Loaded the trained model")
    except Exception as e:
        print("The trained model is not found. Check again or train again")
        print(e)
        print("Completed error")
    preditedLabel = [] # a list to store the labels of the given movie
    for s in li:
        s = s.lower().strip() # convert to lower and remove the spaces
        # convert to the vectors
        word_id = []
        s = s.split(" ")
        for word in s:
            if word in word_to_id.keys():
                value = word_to_id[word]
                word_id.append(value)
        # convert to numpy array
        arr = np.array([word_id])
        # predict it
        result = reconstructed_model.predict_classes(arr)
        # get the label
        preditedLabel.append(result.tolist()[0][0])
        
    # find the sentiment of the movie based on the sentiment predicted from that reviews
    count_of_negativeReviews = preditedLabel.count(0)
    count_of_positiveReviews = preditedLabel.count(1)
    percentageOfPositiveReview = (count_of_positiveReviews)/(len(preditedLabel))
    percentageOfPositiveReview = int(percentageOfPositiveReview * 100)
    return percentageOfPositiveReview
