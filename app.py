import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

@app.route("/")
@app.route("/login")
def home():
    # Check if user is logged in
    if "user" in session:
        session.pop("user")  # Logout the user if logged in

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")

from flask import request

# Update your profile route to handle pagination
from math import ceil

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        page = request.args.get("page", default=1, type=int)
        per_page = 10

        user_recipes = list(mongo.db.recipes.find({"created_by": session["user"]})
                            .skip((page - 1) * per_page).limit(per_page))

        # Calculate total number of pages
        total_recipes = mongo.db.recipes.count_documents({"created_by": session["user"]})
        total_pages = ceil(total_recipes / per_page)

        return render_template("profile.html", username=username, user_recipes=user_recipes, total_pages=total_pages)

    return redirect(url_for("login"))


# app.py

@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))  # Redirect to the login page after logging out


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "ingredients": request.form.get("ingredients"),
            "description": request.form.get("description"),
            "cooking_instructions": request.form.get("cooking_instructions"),
            "preparation_time": request.form.get("preparation_time"),
            "serving_size": request.form.get("serving_size"),
            "created_by": session["user"]
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe added successfully!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("add_recipe.html")

@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})
    flash("Recipe deleted successfully!")
    return redirect(url_for("profile", username=session["user"]))

@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    if request.method == "POST":
        updated_recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "ingredients": request.form.get("ingredients"),
            "description": request.form.get("description"),
            "cooking_instructions": request.form.get("cooking_instructions"),
            "preparation_time": request.form.get("preparation_time"),
            "serving_size": request.form.get("serving_size"),
            "created_by": session["user"]
        }
        mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, {"$set": updated_recipe})
        flash("Recipe updated successfully!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("edit_recipe.html", recipe=recipe)


@app.route("/view_recipe/<recipe_id>", methods=["GET", "POST"])
def view_recipe(recipe_id):
    # Retrieve the recipe details from the database
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    if not recipe:
        flash("Recipe not found")
        return redirect(url_for("profile", username=session["user"]))
    
    if request.method == "POST":
        # Handle delete request
        if request.form.get("action") == "delete":
            mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})
            flash("Recipe deleted successfully!")
            return redirect(url_for("profile", username=session["user"]))
        # Handle edit request
        elif request.form.get("action") == "edit":
            return redirect(url_for("edit_recipe", recipe_id=recipe_id))
    
    return render_template("view_recipe.html", recipe=recipe)



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)


