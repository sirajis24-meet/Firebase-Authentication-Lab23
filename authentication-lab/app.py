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
  "databaseURL" : "https://sheeple-85021-default-rtdb.europe-west1.firebasedatabase.app/",
}

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth() 
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "login failed"

    return render_template("signin.html", error = error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        username = request.form['username']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {'fullname' : fullname, 'username' : username, 'bio' : bio}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "auth failed"
    return render_template("signup.html", error = error)


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error = ""
    if request.method == "POST" :
        Text = request.form['Text1']
        Title = request.form['Title']
        try:
            UID = login_session['user']['localId']
            tweet = {'Title' : Title, 'Text' : Text, 'UID' : UID}
            db.child("Tweets").push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            error = "coudnt add"
    return render_template("add_tweet.html", error = error)

@app.route('/all_tweets')
def all_tweets():
    return render_template("Tweets.html", tweets = db.child('Tweets').get().val())


if __name__ == '__main__':
    app.run(debug=True)