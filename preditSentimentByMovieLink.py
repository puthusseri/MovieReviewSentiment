# TODO :  BELOW STEPS HAS TO BE DONE FIRST ONLY ONCE
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from selenium import webdriver
from bs4 import BeautifulSoup as bs4
from urllib.request import urlopen
import time

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
# movie_name = input("Enter the movie name : ")

def findTheSentimentOfThisMovie(reviewsLink):
    browser = webdriver.Chrome('./chromedriver')


    # url_of_movie = "https://www.imdb.com/find?q="+movie_name+"&ref_=nv_sr_sm"
    # browser.get(url_of_movie)
    # time.sleep(3)
    # parentTable = browser.find_element_by_tag_name("table") # take the list of movies
    # linkToMovie = parentTable.find_element_by_tag_name("a") # select the first movie

    # # get the title from the review hyperlink 
    # titleName = linkToMovie.get_attribute("href").split("/")[4]
    # # append the title to the home url to get the reviews
    # reviewsLink = "https://www.imdb.com/title/"+titleName+"/reviews"
    browser.get(reviewsLink) # load the review page

    # create an empty list to store the reviews of the movie
    listOfReview = []

    print("Scrapping process starts.")
    try:
        while True:
            loadMoreButton = browser.find_element_by_css_selector(".ipl-load-more__button")
            if loadMoreButton is not None:
                loadMoreButton.click()
                time.sleep(3)
            else:
                break
    except:
        print("Compeleted the loading of all the reviews of the movie")

    try:
        while True:
            time.sleep(1)
            browser.find_element_by_css_selector("expander-icon-wrapper.spoiler-warning__control").click()
    except:
        print("Completed the expansion of the reviews..")


    # load all the reviews to the list of reviews
    li  = browser.find_elements_by_css_selector(".text.show-more__control")
    len(li)
    count = 0 
    validReviews = []
    for i in li:
        if len(i.text) == 0:
            count += 1
        else:
            validReviews.append(i.text.replace("\n" , " "))

    print("Total number of reviews got is : ",count, "  Actually it i s ",len(li))

    # dave to a file
    f = open("review.txt","w")
    data = ";".join(validReviews)
    f.write(data)
    f.close()
    # quit the browser instance
    # browser.quit()
    # FIND SENTIMENTSE OF THE REVIEWS


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
        reconstructed_model.load_weights("./weigts.h5")
        print("Loaded the trained model")
    except Exception as e:
        print("The trained model is not found. Check again or train again")
        print(e)
    preditedLabel = [] # a list to store the labels of the given movie
    countOfReview = 0
    for s in li:
        countOfReview += 1 
        print(f"Processing {countOfReview} ")
        try:
            s = s.text
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
        except:
            print("This review cannot be processed")
            countOfReview -= 1

        
    # find the sentiment of the movie based on the sentiment predicted from that reviews
    count_of_negativeReviews = preditedLabel.count(0)
    count_of_positiveReviews = preditedLabel.count(1)
    percentageOfPositiveReview = (count_of_positiveReviews)/(len(preditedLabel))
    percentageOfPositiveReview = int(percentageOfPositiveReview * 100)
    print(f"Analysed the  {(len(preditedLabel))} number of reviews and got the number of positive reviews as {count_of_positiveReviews}")
    browser.quit()
    result = ""
    if percentageOfPositiveReview  >50:
        result = "Positive Review"
    else:
        result = "Negative Review"
    
    return result

# movie_name = "pokiri"
# findTheSentimentOfThisMovie(movie_name)