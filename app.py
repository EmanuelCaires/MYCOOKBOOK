import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
from urllib.parse import quote_plus

app = Flask(__name__)

# Encode the username and password for MongoDB URI
username = "emanuelcaires1"
password = "emanuelcaires1"
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get(
    "MONGO_URI",
    f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.wmcpp51.mongodb.net/myCookbookDB?retryWrites=true&w=majority",
)
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Create 'users' collection if not exists
with app.app_context():
    if 'users' not in mongo.db.list_collection_names():
        users = mongo.db.users
        users.insert_one({'username': 'your_username', 'password': 'your_password'})

# ...

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({'username': username, 'password': password})
        if user:
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))




