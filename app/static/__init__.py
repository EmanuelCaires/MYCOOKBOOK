# app/__init__.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
from app.db import get_db

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://your_username:your_password@localhost:27017/recipe_app'
app.config['SECRET_KEY'] = 'your_secret_key'
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




