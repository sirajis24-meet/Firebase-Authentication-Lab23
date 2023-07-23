from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase




Config = {

  "apiKey": "AIzaSyAm3lbYU01er9JDLIXxLCWcHdrgmNCRu_0",

  "authDomain": "sheeple-85021.firebaseapp.com",

  "projectId": "sheeple-85021",

  "storageBucket": "sheeple-85021.appspot.com",

  "messagingSenderId": "630439104792",

  "appId": "1:630439104792:web:848393d59ae654ced58e6d",

  "databaseURL" : "",

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth() 

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form('email')
        password = request.form('password')
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)