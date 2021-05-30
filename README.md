# MovieReviewSentiment

# Scrapping
Just trying to scrap imdb and anlysing the review sentiment.

### Installation

 - This project requires [Python3](https://www.python.org/downloads/) 
 - Install [anaconda](https://www.anaconda.com/products/individual)
 - To reproduce the environment, run the below code after installing the anaconda<br />
 ```sh
conda env create -f environment.yml

 ```
 - Now all the dependencies will be downloaded in your system
 - Activate the environment by<br/>
 

 - Download the correct version of the [chrome driver](https://chromedriver.chromium.org/downloads) and put the driver in this directory
 - Go to your chrome browser and check the version in it. Download the chrome driver for the same version.<br/>
 - Run the server.py ```python server.py```<br/>

### Setting Database

 - I had used two tables here in the database named ```imdb```. So create a database and give all the privilages to it.
 - Need two tables

```mysql
CREATE TABLE USER(USER_ID INT PRIMARY KEY AUTO_INCREMENT,
        NAME VARCHAR(20), 
        USERNAME VARCHAR(20), 
        PASSWORD VARCHAR(20)
);
CREATE TABLE TRANSACTIONS(TRANSACTION_ID INT PRIMARY KEY AUTO_INCREMENT,
        USER_ID VARCHAR(20),
        TYPE_OF_CONTENT VARCHAR(20),
        REVIEW VARCHAR(200),
        FEEDBACK VARCHAR(50)

);
```

### Todos

 - Contact page : Handling in server side.
 - Change the UI contents

