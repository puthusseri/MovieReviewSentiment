# the flask server for the dashboard application
from flask import *
import preditSentimentByMovieName as byName
import preditSentimentByMovieLink as byLink
import mainCode as mainCode
# import language_tool_python
# tool = language_tool_python.LanguageTool('en-US')

import mysql.connector
app = Flask(__name__)

@app.route("/")
def loginPage():
    return render_template("login.html")

@app.route("/registerUser")
def registerUser():
    # define the method for registration process
    mydb = mysql.connector.connect(
    host="localhost",
    user="vyshak-zt515",
    password="password",
    database="imdb"
    )
    mycursor = mydb.cursor()
    name = request.args.get('name')
    username = request.args.get('username')
    password = request.args.get('password')
    sql = "INSERT INTO USER(NAME, USERNAME, PASSWORD) VALUES (%s, %s,%s)"
    val = (name, username, password)
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return render_template("login.html" ,messageFromServer="Registration Successful")

@app.route("/loginToUser")
def loginToUser():
    # define the method for login process
    mydb = mysql.connector.connect(
    host="localhost",
    user="vyshak-zt515",
    password="password",
    database="imdb"
    )
    mycursor = mydb.cursor()
    username = request.args.get('username')
    password = request.args.get('password')
    sql = "SELECT * FROM USER WHERE USERNAME = '"+username+"' AND PASSWORD = '"+ password +"';"

    mycursor.execute(sql)
    account = mycursor.fetchall()
    mydb.close()
    if len(account) > 0:
        # the login is valid
        # check if the login is by admin
        if account[0][1] == "admin":
            resp = make_response(render_template('admin.html'))
            resp.set_cookie('name', 'admin')
            resp.set_cookie('user_id', str(account[0][0]))
        else:
            resp = make_response(render_template('index.html'))
            resp.set_cookie('name', account[0][1])
            resp.set_cookie('user_id', str(account[0][0]))
        
        return resp
    else:
        pass
    return render_template("login.html",messageFromServer="Login Unsuccessful")



@app.route('/logoutButton')
def logoutButton():
    resp = make_response(render_template('login.html'))
    resp.set_cookie('name', " ")
    return resp
@app.route('/index')
def indexpage():
    return render_template("index.html")
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/contactPage')
def contactPage():
    return render_template("contactPage.html")

@app.route('/redirectToSearchMovieByName')
def redirectToSearchMovieByName():
    return render_template("searchMovieByName.html")

@app.route('/redirectToSearchMovieByLink')
def redirectToSearchMovieByLink():
    return render_template("searchMovieByLink.html")
@app.route('/loadSearchById')
def redirectToloadSearchById():
    return render_template("searchByIdTransactions.html")


@app.route('/goToEnterMovieReview')
def goToEnterMovieReview():
    return render_template("checkByReview.html")



@app.route('/analyseReview')
def analyseReview():
    #  predit the sentiment of the entered movie review
    '''
    @return 1 or 0
    '''
    movie_review = request.args.get("movie_review")
    # print(movie_review)
    # check if the review 
    # matches = tool.check(movie_review)
    # if len(matches) > 0:
        # the review is not having good grammer
    #     print(f"Invalid Grammer. Number of grammer errors are : {len(matches)}")
    #     return "Invalid Grammer"
    # print("There are no grammer mistakes in the review text")
    result = mainCode.mainMethod(movie_review)
    if result == "Positive Review":
        return "1"
    # else:
    #     return "0"

    return "0"

@app.route('/submitMovieName')
def submitMovieName():
    #  predit the sentiment of the entered movie name
    movieName = request.args.get("movieName")
    print("name of the movie to search is "+movieName)
    result = byName.findTheSentimentOfThisMovie(movieName)
    return result


@app.route('/submitMovieLink')
def submitMovieLink():
    #  predit the sentiment of the entered movie link
    movieLink = request.args.get("movieLink")
    print("name of the link to search is :  "+movieLink)
    result = byLink.findTheSentimentOfThisMovie(movieLink)
    return result
@app.route('/contactMeForm')
def contactPageDetails():
    # TODO : STORE THE DETAILS OF THE CONTACT PAGE TO THE SERVER
    return "True"



@app.route('/storeReviewFeedBackToDB')
def storeReviewFeedBackToDB():
    #  Store the content to the database
    movie_review = request.args.get("movie_review")
    typeOfContent = request.args.get("typeOfContent")
    feedback = request.args.get("feedback")
    user_id = request.args.get("user_id")
    
    # define the method for db insert process
    mydb = mysql.connector.connect(
    host="localhost",
    user="vyshak-zt515",
    password="password",
    database="imdb"
    )
    mycursor = mydb.cursor()
    
    sql = "INSERT INTO TRANSACTIONS(USER_ID, TYPE_OF_CONTENT, REVIEW, FEEDBACK) VALUES (%s, %s,%s, %s)"
    val = (user_id, typeOfContent, movie_review, feedback)
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    
    return "True"

@app.route('/searchTranasactionByid')
def searchTranasactionByid():
    user_id = request.args.get("user_id")
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="vyshak-zt515",
    password="password",
    database="imdb"
    )
    mycursor = mydb.cursor()
    
    sql = "SELECT * FROM TRANSACTIONS WHERE USER_ID = '"+user_id+"';"
    mycursor.execute(sql)
    account = mycursor.fetchall()
    
    mydb.close()

    return render_template("tables.html", account = account)


@app.route('/searchTranasactions')
def searchTranasactions():
    user_id = request.args.get("user_id")
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="vyshak-zt515",
    password="password",
    database="imdb"
    )
    mycursor = mydb.cursor()
    
    sql = "SELECT * FROM TRANSACTIONS;"
    mycursor.execute(sql)
    account = mycursor.fetchall()
    
    mydb.close()

    return render_template("tables.html", account = account)

if __name__ == "__main__":
    app.run(threaded=False, debug = True)
