import re
import pandas as pd

# -----------------------------------------------------
# INGREDIENT LIST
# -----------------------------------------------------

INGREDIENTS = {

    "chicken": [
        "chicken",
        "grilled chicken",
        "fried chicken",
        "crispy chicken",
        "chicken breast",
        "chicken thigh",
        "chicken wings",
        "chicken strips",
        "chicken fillet"
    ],
    "pork":[
        "pork"
    ],

    "paneer": [
        "paneer",
        "cottage cheese"
    ],

    "cheese": [
        "cheese",
        "mozzarella",
        "cheddar",
        "parmesan"
    ],

    "mushroom": [
        "mushroom",
        "button mushroom",
        "shiitake",
        "portobello"
    ],

    "beef": [
        "beef",
        "beef patty",
        "ground beef",
        "steak"
    ],

    "fish": [
        "fish",
        "salmon",
        "tuna",
        "cod"
    ],

    "fruits": [
        "Banana",
        "Guava",
        "Mango",
        "Pineapple",
        "Graps",
        "Apple",
    ],

    "coffee": [
        "Espresso","Americano","Cappuccino","Latte","Flat White","Macchiato","Mocha","Cortado","Ristretto","Lungo","Affogato","Irish Coffee","Cold Brew","Iced Coffee","Nitro Cold Brew","Turkish Coffee","French Press Coffee","Pour Over Coffee","Drip Coffee","Aeropress Coffee","Moka Pot Coffee","Vienna Coffee","Breve","Red Eye","Black Eye","Cafe au Lait","Piccolo Latte","Long Black","Doppio","Single Espresso","Caramel Macchiato","Vanilla Latte","Hazelnut Latte","White Mocha","Cafe Cubano","Cafe Bombon","Dirty Chai Latte","Bulletproof Coffee","Frappe","Frappuccino","Iced Latte","Iced Americano","Iced Mocha","Iced Cappuccino","Honey Latte","Spanish Latte","Coconut Latte","Oat Milk Latte","Almond Milk Latte","Decaf Coffee", "Coffee"
    ],


    "vegitables": [
        "Vegitable",
        "Green Beans",
        "green beans"
    ],

    "flour, water, yeast, salt, suger": ["bagel","cake","pastry","muffin","donut","cookie"],
    "flour, water" :["roti","naan","kulcha"],

    "shrimp": [
        "shrimp",
        "prawn",
        "prawns"
    ],

    "butter" :[
        "butter",
        "buttery"
    ],
    "chocolate" : [
        "chocolaty",
        "choco",
        "chocolate"
    ],

    "egg": [
        "egg",
        "boiled egg",
        "fried egg"
    ],

    "rice": [
        "rice",
        "fried rice",
        "steamed rice"
    ],

    "garlic": [
        "garlic",
        "garlic cloves"
    ],

    "onion": [
        "onion",
        "red onion",
        "white onion"
    ],

    "tomato": [
        "tomato",
        "tomatoes"
    ]
}

# -----------------------------------------------------
# DISH TYPE KEYWORDS
# -----------------------------------------------------

DISH_TYPES = {
    "pizza": "Pizza",
    "burger": "Burger",
    "pasta": "Pasta",
    "noodle": "Noodles",
    "noodles": "Noodles",
    "fried rice": "Rice",
    "rice": "Rice",
    "curry": "Curry",
    "biryani": "Biryani",
    "sandwich": "Sandwich",
    "coffee": "Coffee",
    "tea": "Tea",
    "shake": "Shake",
    "juice": "Juice",
    "salad": "Salad",
    "steak": "Steak",
    "soup": "Soup",
    "dessert": "Dessert",
    "cake": "Cake",
    "ice cream": "Ice Cream",
    "wrap": "Wrap",
    "roll": "Roll",
    "sushi": "Sushi"
}

# -----------------------------------------------------
# NON-VEG INGREDIENTS
# -----------------------------------------------------

NON_VEG = {
    "chicken",
    "beef",
    "mutton",
    "lamb",
    "pork",
    "bacon",
    "ham",
    "sausage",
    "pepperoni",
    "fish",
    "salmon",
    "tuna",
    "shrimp",
    "prawn",
    "crab",
    "lobster"
}





# -----------------------------------------------------
# EXTRACT INGREDIENTS
# -----------------------------------------------------

def extract_ingredients(text):

    if pd.isna(text):
        return ""

    text = text.lower()

    found = []

    for ingredient, keywords in INGREDIENTS.items():

        for keyword in keywords:

            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, text):
                found.append(ingredient)
                break      # don't add "chicken" twice

    return ", ".join(found)

# -----------------------------------------------------
# DISH CATEGORY
# -----------------------------------------------------

def detect_dish_type(text):

    if pd.isna(text):
        return "Other"

    text = text.lower()

    for keyword, category in DISH_TYPES.items():

        if keyword in text:
            return category

    return "Other"


# -----------------------------------------------------
# VEG / NON VEG
# -----------------------------------------------------

def classify_food(ingredients):

    if not ingredients:
        return "Veg"

    ingredient_list = [
        x.strip().lower()
        for x in ingredients.split(",")
        if x.strip()
    ]

    for ingredient in ingredient_list:

        if ingredient in NON_VEG:
            return "Non-Veg"

    return "Veg"

# -----------------------------------------------------
# MAIN FEATURE FUNCTION
# -----------------------------------------------------

def create_features(df):

    df = df.copy()

    # Combine dish name and description

    df["combined_text"] = (
        df["dish_name"].fillna("")
        + " "
        + df["description"].fillna("")
    )

    # Ingredient extraction

    df["ingredients"] = df["combined_text"].apply(extract_ingredients)

    # Ingredient count

    df["ingredient_count"] = df["ingredients"].apply(
    lambda x: len(x.split(",")) if x else 0
)

    # Dish category

    df["dish_type"] = df["description"].apply(
        detect_dish_type
    )

    # Veg / Non Veg

    df["food_type"] = df["ingredients"].apply(classify_food)

    # Boolean features

    df["contains_cheese"] = df["ingredients"].apply(
        lambda x: "cheese" in x
    )

    df["contains_chicken"] = df["ingredients"].apply(
        lambda x: "chicken" in x
    )

    df["contains_paneer"] = df["ingredients"].apply(
        lambda x: "paneer" in x
    )

    return df


# -----------------------------------------------------
# SAVE FEATURED DATASET
# -----------------------------------------------------

if __name__ == "__main__":

    input_file = "data/cleaned_menu_data.csv"
    output_file = "data/featured_menu_data.csv"

    df = pd.read_csv(input_file)

    df = create_features(df)

    df.to_csv(output_file, index=False)

    print("Feature engineering completed.")

    print(df.head())