import os
from flask import Flask
if os.path.exists("env.py"):
    import env


app = Flask(__name__)



@app.route("/")
@app.route("/add_recipe")
def get_recipes():
    recipe= mongo.db.recipes.find()
    return render_template("add_recipe.html", recipe=recipe)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)