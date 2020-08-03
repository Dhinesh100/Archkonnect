# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 22:53:13 2020

@author: Dinesh
"""

from flask import Flask, flash, request, render_template, redirect, url_for, session
from flask_mail import Mail, Message
import pyrebase, re

config = {
    "apiKey": "AIzaSyC7G0cOoZxm8d6Tf2wXmydvA4IoBRnlgTw",
    "authDomain": "archkonnect-705a4.firebaseapp.com",
    "databaseURL": "https://archkonnect-705a4.firebaseio.com",
    "projectId": "archkonnect-705a4",
    "storageBucket": "archkonnect-705a4.appspot.com",
    "messagingSenderId": "295221657522",
    "appId": "1:295221657522:web:3dfafe566d4829bf9f6eab",
    "measurementId": "G-E4WCS1E0YF"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

app = Flask(__name__)

app.secret_key = "super secret key"

@app.route('/index.html')
def homepage():
    return render_template('index.html')

@app.route('/subscribe.html', methods=["POST", "GET"])
def subscribepage_form():
    error1 = None
    error2 = None 
    snackbar = None
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        regex = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        if not name:
            if not email:
                nameerr = 'This field cannot be empty'
                emailerr = 'This field cannot be empty'
                return render_template('subscribe.html', nameerr = nameerr, emailerr = emailerr)
            else:
                nameerr = 'This field cannot be empty'
                return render_template('subscribe.html', nameerr = nameerr, email = email)
        elif not email:
            emailerr = 'This field cannot be empty'
            return render_template('subscribe.html', emailerr = emailerr, name = name)
        elif not re.search(regex, email):
                emailerr = 'Kindly enter a valid email'
                return render_template('subscribe.html', emailerr = emailerr, name = name)
        else:
            if db.child("Users").child(name).get().key:
                error1 = "The given email already exists"
                error2 = "in subscription list"
            else:
                db.child("Users").update({name:email})
                snackbar = "You have succesfully subscribed"
                return render_template('subscribe.html', snackbar = snackbar)
    return render_template('subscribe.html', error1 = error1, error2 = error2)

@app.route('/comments.html')
def commentpage():
    return render_template('comments.html')

@app.route('/about.html')
def aboutpage():
    return render_template('about.html')
 
if __name__ == '__main__':
    app.run()