from flask import *
import mainCode as mainCode
app = Flask(__name__)

@app.route('/')
def success():
   return render_template("index.html")

@app.route('/predict',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      reviewText = request.form['userInput']
      print(reviewText)
      result = mainCode.mainMethod(reviewText)
      return render_template("index.html", result = result)
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

# @app.route('/predicssst', methods = ['GET'])
# def predictTheSentiments():
#     if request.methods == 'GET':
#         reviewText=request.form.get("userInput")
#         print(reviewText)
#         result = mainCode.mainMethod(reviewText)
#         return render_template("index.html", result = result)

if __name__ == "__main__":
    app.run(threaded=False)
