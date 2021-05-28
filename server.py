# the flask server for the dashboard application
from flask import *
import preditSentimentByMovieName as byName
import preditSentimentByMovieLink as byLink
import mainCode as mainCode
import language_tool_python
tool = language_tool_python.LanguageTool('en-US')


app = Flask(__name__)

@app.route('/')
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
    matches = tool.check(movie_review)
    if len(matches) > 0:
        # the review is not having good grammer
        print(f"Invalid Grammer. Number of grammer errors are : {len(matches)}")
        return "Invalid Grammer"
    print("There are no grammer mistakes in the review text")
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


if __name__ == "__main__":
    app.run(threaded=False)
