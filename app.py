# app/__init__.py
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb+srv://emanuelcaires1:emanuelcaires1@cluster0.wmcpp51.mongodb.net/myCookbookDB?retryWrites=true&w=majority")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Ensure the connection to the MongoDB database
with app.app_context():
    try:
        mongo.db.list_collection_names()
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")

# ...

if __name__ == '__main__':
    # Use the PORT environment variable if available, otherwise default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)





