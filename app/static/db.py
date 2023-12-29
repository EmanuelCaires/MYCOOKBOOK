# app/db.py
from flask_pymongo import PyMongo

mongo = PyMongo()

def get_db():
    return mongo.db
