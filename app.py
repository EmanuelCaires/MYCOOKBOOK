# app/__init__.py
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
from urllib.parse import quote_plus
import pymongo.uri_parser

app = Flask(__name__)

# Rest of your code...


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
username = "emanuelcaires1"
password = "emanuelcaires1"
cluster_url = "cluster0.wmcpp51.mongodb.net"
database_name = "myCookbookDB"
parsed_uri = pymongo.uri_parser.parse_uri(os.environ.get("MONGO_URI", f"mongodb+srv://{username}:{password}@{cluster_url}/{database_name}?retryWrites=true&w=majority"))
parsed_uri["username"] = quote_plus(parsed_uri["username"])
parsed_uri["password"] = quote_plus(parsed_uri["password"])
app.config["MONGO_URI"] = pymongo.uri_parser.unparse_uri(parsed_uri)

app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Create 'users' collection if not exists
with app.app_context():
    if 'users' not in mongo.db.list_collection_names():
        users = mongo.db.users
        users.insert_one({'username': 'your_username', 'password': 'your_password'})

# ...

# Your routes go here...

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




