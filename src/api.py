import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env.local"))

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SPOONACULAR_BASE = "https://api.spoonacular.com"

def identify_ingredients_from_image(image_bytes):
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
    payload = {
        "model": "claude-opus-4-5",
        "max_tokens": 256,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_b64
                        }
                    },
                    {
                        "type": "text",
                        "text": "List only the raw or packaged food items visible in this fridge photo that could be used as cooking ingredients. One item per line, plain names only, no quantities or extra commentary. Exclude vague items like leftovers, containers, or baby food. If you cannot identify any food items, respond with an empty string."
                    }
                ]
            }
        ]
    }

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json=payload
    )
    response.raise_for_status()
    text = response.json()["content"][0]["text"]
    ingredients = [line.strip() for line in text.splitlines() if line.strip()]
    return ingredients

def find_recipes_by_ingredients(ingredients, recipe_types=None, number=20):
    params = {
        "apiKey": API_KEY,
        "ingredients": ",".join(ingredients),  # note: changed from includeIngredients
        "number": number,
        "ranking": 2,          # 1 = maximize used ingredients, 2 = minimize missing ingredients
        "ignorePantry": True,  # ignores common pantry items like salt, water, oil
    }

    response = requests.get(API_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    recipes = response.json()
    if not isinstance(recipes, list):
        raise Exception(f"Unexpected response format: {recipes}")
    return recipes

def get_recipe_information(recipe_id):
    url = f"{SPOONACULAR_BASE}/recipes/{recipe_id}/information"
    params = {"apiKey": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    return response.json()