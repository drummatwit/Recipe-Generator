# Recipe Generator

A web app that generates recipes based on ingredients you have on hand. Type ingredients manually or scan your fridge with your camera — the app uses AI to identify food items from the photo and automatically populates the ingredient list.

![Recipe Generator](https://img.shields.io/badge/Python-3.10+-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey) ![Claude API](https://img.shields.io/badge/Claude-Vision_API-violet)

---

## Features

- **Fridge Scanner** — upload a photo of your fridge and Claude's vision API identifies the ingredients automatically
- **Ingredient Tags** — add, remove, and manage ingredients with a tag-based UI
- **Meal Type Filtering** — filter results by breakfast, main course, dessert, soup, and more
- **Recipe Detail Pages** — view full ingredients, step-by-step instructions, prep time, and servings
- **Dark UI** — modern dark theme built with vanilla CSS

---

## Tech Stack

- **Backend** — Python, Flask
- **Frontend** — HTML, CSS, vanilla JavaScript
- **Recipe Data** — [Spoonacular API](https://spoonacular.com/food-api)
- **Ingredient Recognition** — [Anthropic Claude API](https://www.anthropic.com) (claude-opus-4-5 vision)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/recipe-generator.git
cd recipe-generator
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install flask requests python-dotenv
```

### 4. Get your API keys

**Spoonacular** (recipe data)
- Sign up at [spoonacular.com/food-api](https://spoonacular.com/food-api)
- Copy your API key from the dashboard

**Anthropic** (fridge scanner)
- Sign up at [console.anthropic.com](https://console.anthropic.com)
- Create an API key under API Keys
- Set a monthly spend limit under Settings → Limits

### 5. Create your environment file

Create a `.env.local` file in the **parent directory** of the project (one level above `app.py`):

```
API_KEY=your_spoonacular_key_here
API_URL=https://api.spoonacular.com/recipes/findByIngredients
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### 6. Run the app

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Project Structure

```
recipe-generator/
├── app.py               # Flask routes
├── api.py               # Spoonacular and Anthropic API calls
├── static/
│   └── style.css        # Dark theme stylesheet
└── templates/
    ├── index.html       # Home page with ingredient input and fridge scanner
    ├── results.html     # Recipe results grid
    └── recipe.html      # Individual recipe detail page
```

---

## Usage

**Manual ingredients**
1. Type an ingredient into the input field and click **+ Add** or press Enter
2. Remove any ingredients by clicking **×** on a tag
3. Optionally select a meal type
4. Click **Find Recipes**

**Fridge scanner**
1. Click **Scan Fridge** and select a photo of your fridge
2. The app sends it to Claude's vision API
3. Identified ingredients appear as tags automatically
4. Remove any false positives, then click **Find Recipes**

---

## Notes

- The fridge scanner works best with clear, well-lit photos
- For best recipe results, keep your ingredient list focused — remove items you don't want to cook with before searching
