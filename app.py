import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def home():
    return render_template("base.html")
    

@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        # Get form data
        recipe_name = request.form.get("name")
        recipe_description = request.form.get("description")

        # Insert data into MongoDB
        mongo.db.recipes.insert_one({
            "name": recipe_name,
            "description": recipe_description
        })

        # Redirect to the recipe list page or another appropriate page
        return redirect(url_for('recipe_list'))

    return render_template("add_recipe.html")

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
