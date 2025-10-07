import requests
import os
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env.local"))

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

print("🔑 API Key loaded:", "✅ Found" if API_KEY else "❌ Missing")

def find_recipes_by_ingredients(ingredients, recipe_type=None, number=20):
    url = API_URL
    params = {
        "apiKey": API_KEY,
        "includeIngredients": ",".join(ingredients),
        "number": number,
        "instructionsRequired": True, 
        "addRecipeInformation": True
    }

    if recipe_type:
        params["type"] = recipe_type

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    data = response.json()
    recipes = data.get("results", [])

    if recipe_type:
        filtered = []
        for r in recipes:
            if "dishTypes" in r and recipe_type.lower() in [dt.lower() for dt in r["dishTypes"]]:
                filtered.append(r)
        return filtered
    return recipes

def get_recipe_information(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    data = response.json()
    return data