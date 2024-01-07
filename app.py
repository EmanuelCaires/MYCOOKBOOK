from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['recipe_database']
recipes = db['recipes']

# Create necessary routes
@app.route('/')
def home():
    recipe_list = recipes.find()
    return render_template('recipes.html', recipe_list=recipe_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Add your login logic here
    pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Add your register logic here
    pass

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        new_recipe = {
            'title': request.form['title'],
            'ingredients': request.form['ingredients'],
            'directions': request.form['directions']
        }
        recipes.insert_one(new_recipe)
        return redirect(url_for('home'))
    return render_template('add_recipe.html')

@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    if request.method == 'POST':
        updated_recipe = {
            'title': request.form['title'],
            'ingredients': request.form['ingredients'],
            'directions': request.form['directions']
        }
        recipes.update_one({'_id': ObjectId(recipe_id)}, {'$set': updated_recipe})
        return redirect(url_for('home'))
    recipe = recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form['query']
    recipe_list = recipes.find({'title': {'$regex': query, '$options': 'i'}})
    return render_template('recipes.html', recipe_list=recipe_list)

if __name__ == '__main__':
    app.run(debug=True)
