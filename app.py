from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://emanuelcaires1:emanuelcaires1@cluster0.wmcpp51.mongodb.net/?'
mongo = PyMongo(app)

def login():
    if request.method == 'POST':
        # Handle the login process here
        return render_template('login.html')

# Add your other routes and functions here

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        # Add your code to insert a new recipe into the database
        return redirect(url_for('home'))
    return render_template('add_recipe.html')

@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    if request.method == 'POST':
        # Add your code to update the recipe in the database
        return redirect(url_for('home'))
    # Add your code to retrieve the recipe from the database
    return render_template('edit_recipe.html')