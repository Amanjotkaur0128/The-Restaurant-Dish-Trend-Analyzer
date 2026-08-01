import re

import pandas as pd


# Canonical ingredient names mapped to common menu wording.
INGREDIENTS = {
    "chicken": ["chicken", "chicken breast", "chicken thigh", "chicken wings", "chicken fillet"],
    "paneer": ["paneer", "cottage cheese"],
    "cheese": ["cheese", "mozzarella", "cheddar", "parmesan"],
    "mushroom": ["mushroom", "mushrooms", "shiitake", "portobello"],
    "beef": ["beef", "beef patty", "ground beef"],
    "pork": ["pork", "bacon", "ham", "sausage", "pepperoni"],
    "fish": ["fish", "salmon", "tuna", "cod"],
    "shrimp": ["shrimp", "prawn", "prawns"],
    "egg": ["egg", "eggs", "omelette", "omelet"],
    "rice": ["rice", "risotto"],
    "potato": ["potato", "potatoes", "fries"],
    "tomato": ["tomato", "tomatoes"],
    "onion": ["onion", "onions"],
    "garlic": ["garlic"],
    "spinach": ["spinach"],
    "corn": ["corn"],
    "butter": ["butter", "buttery"],
    "milk": ["milk", "oat milk", "almond milk"],
    "cream": ["cream", "creamy"],
    "chocolate": ["chocolate", "choco", "cocoa"],
    "coffee": ["coffee", "espresso", "americano", "cappuccino", "latte", "mocha", "cold brew"],
    "tea": ["tea", "chai"],
    "fruit": ["banana", "guava", "mango", "pineapple", "grapes", "apple"],
    "vegetables": ["vegetable", "vegetables", "green beans"],
}

DISH_TYPES = {
    "pizza": "Pizza", "burger": "Burger", "pasta": "Pasta", "noodles": "Noodles",
    "noodle": "Noodles", "fried rice": "Rice", "rice": "Rice", "curry": "Curry",
    "biryani": "Biryani", "sandwich": "Sandwich", "coffee": "Coffee", "tea": "Tea",
    "shake": "Shake", "juice": "Juice", "salad": "Salad", "steak": "Steak",
    "soup": "Soup", "dessert": "Dessert", "cake": "Cake", "ice cream": "Ice Cream",
    "wrap": "Wrap", "roll": "Roll", "sushi": "Sushi",
}

NON_VEG = {"chicken", "beef", "pork", "fish", "shrimp", "egg"}


def extract_ingredients(text):
    """Return unique canonical ingredients found in a dish name or description."""
    if pd.isna(text):
        return ""

    text = str(text).lower()
    found = []
    for ingredient, keywords in INGREDIENTS.items():
        if any(re.search(r"\b" + re.escape(keyword) + r"\b", text) for keyword in keywords):
            found.append(ingredient)
    return ", ".join(found)


def get_top_ingredients(df, top_n=15):
    """Return the most frequent extracted ingredients as a chart-ready DataFrame."""
    if "ingredients" not in df.columns:
        return pd.DataFrame(columns=["Ingredient", "Count"])

    ingredients = df["ingredients"].fillna("").str.split(",").explode().str.strip().str.lower()
    ingredients = ingredients[ingredients.ne("")]
    if ingredients.empty:
        return pd.DataFrame(columns=["Ingredient", "Count"])

    return ingredients.value_counts().head(top_n).rename_axis("Ingredient").reset_index(name="Count")


def detect_dish_type(text):
    if pd.isna(text):
        return "Other"
    text = str(text).lower()
    for keyword, category in DISH_TYPES.items():
        if keyword in text:
            return category
    return "Other"


def classify_food(ingredients):
    found = {item.strip().lower() for item in str(ingredients).split(",") if item.strip()}
    return "Non-Veg" if found & NON_VEG else "Veg"


def create_features(df):
    df = df.copy()
    df["combined_text"] = df["dish_name"].fillna("") + " " + df["description"].fillna("")
    df["ingredients"] = df["combined_text"].apply(extract_ingredients)
    df["ingredient_count"] = df["ingredients"].apply(lambda value: len(value.split(",")) if value else 0)
    df["dish_type"] = df["combined_text"].apply(detect_dish_type)
    df["food_type"] = df["ingredients"].apply(classify_food)
    df["contains_cheese"] = df["ingredients"].str.contains(r"\bcheese\b", regex=True, na=False)
    df["contains_chicken"] = df["ingredients"].str.contains(r"\bchicken\b", regex=True, na=False)
    df["contains_paneer"] = df["ingredients"].str.contains(r"\bpaneer\b", regex=True, na=False)
    return df


if __name__ == "__main__":
    input_file = "data/cleaned_menu_data.csv"
    output_file = "data/featured_menu_data.csv"
    featured_data = create_features(pd.read_csv(input_file))
    featured_data.to_csv(output_file, index=False)
    print(get_top_ingredients(featured_data).to_string(index=False))
