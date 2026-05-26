from flask import Flask, render_template, request
from api import find_recipes_by_ingredients, get_recipe_information, identify_ingredients_from_image

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ingredients = [item.strip().capitalize() for item in request.form["ingredients"].split(",") if item.strip()]
        recipe_types = request.form.getlist("recipe_type") 
        try:
            recipes = find_recipes_by_ingredients(ingredients, recipe_types=recipe_types, number=20)
        except Exception as e:
            return render_template("index.html", error=str(e))
        return render_template("results.html", recipes=recipes, ingredients=ingredients)
    return render_template("index.html")

@app.route('/scan', methods=['POST'])
def scan():
    if 'image' not in request.files:
        return {"error": "No image uploaded"}, 400
    image_file = request.files['image']
    if image_file.filename == '':
        return {"error": "No image selected"}, 400
    try:
        image_bytes = image_file.read()
        ingredients = identify_ingredients_from_image(image_bytes)
        return {"ingredients": ingredients}
    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    try:
        details = get_recipe_information(recipe_id)
    except Exception as e:
        return render_template("index.html", error=str(e))  

    steps = []
    if details.get("analyzedInstructions"):
        for section in details["analyzedInstructions"]:
            for step in section.get("steps", []):
                if step.get("step"):
                    steps.append(step["step"])
    if steps:
        details["steps"] = steps
        details["instructions"] = None
    elif not details.get("instructions"):
        source_url = details.get("sourceUrl")
        if source_url:
            details["instructions"] = f'<a href="{source_url}" target="_blank">View instructions on source site</a>'
        else:
            details["instructions"] = "No instructions available."

    return render_template("recipe.html", recipe=details)


        
if __name__ == "__main__":
    app.run(debug=False)