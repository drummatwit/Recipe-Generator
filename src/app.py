from flask import Flask, render_template, request, redirect, url_for
from api import find_recipes_by_ingredients, get_recipe_information

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ingredients = [item.strip().capitalize() for item in request.form["ingredients"].split(",") if item.strip()]
        recipe_type = request.form.get("recipe_type")
        recipes = find_recipes_by_ingredients(ingredients, recipe_type=recipe_type, number=20)
        return render_template("results.html", recipes=recipes, ingredients=ingredients)
    return render_template("index.html")

@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    details = get_recipe_information(recipe_id)
    return render_template("recipe.html", recipe=details)

if __name__ == "__main__":
    app.run(debug=True)