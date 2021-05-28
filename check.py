from selenium import webdriver
from bs4 import BeautifulSoup as bs4
from urllib.request import urlopen
import time

import findTheSentimentOfListOfReviews as ff
browser = webdriver.Chrome('./chromedriver')

movie_name = input("Enter the movie name : ")
# movie_name = "pokiri"
url_of_movie = "https://www.imdb.com/find?q="+movie_name+"&ref_=nv_sr_sm"
browser.get(url_of_movie)
time.sleep(3)
parentTable = browser.find_element_by_tag_name("table") # take the list of movies
linkToMovie = parentTable.find_element_by_tag_name("a") # select the first movie

# get the title from the review hyperlink 
titleName = linkToMovie.get_attribute("href").split("/")[4]
# append the title to the home url to get the reviews
reviewsLink = "https://www.imdb.com/title/"+titleName+"/reviews"
browser.get(reviewsLink) # load the review page

# create an empty list to store the reviews of the movie
listOfReview = []


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
        browser.find_element_by_css_selector("expander-icon-wrapper.spoiler-warning__control").click()
except:
    print("Completed the expansion of the review")


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

print(count)

# dave to a file
f = open("review.txt","w")
data = ";".join(validReviews)
f.write(data)
f.close()
