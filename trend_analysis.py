import pandas as pd


# =====================================================
# BASIC STATISTICS
# =====================================================

def get_basic_statistics(df):

    stats = {
        "Total Restaurants": df["restaurant"].nunique(),
        "Total Dishes": len(df),
        "Average Price": round(df["price"].mean(), 2),
        "Minimum Price": round(df["price"].min(), 2),
        "Maximum Price": round(df["price"].max(), 2)
    }

    return stats


# =====================================================
# AVERAGE PRICE PER RESTAURANT
# =====================================================

def average_price_restaurant(df):

    return (
        df.groupby("restaurant")["price"]
        .mean()
        .reset_index()
        .sort_values("price", ascending=False)
    )


# =====================================================
# NUMBER OF DISHES PER RESTAURANT
# =====================================================

def dish_count_restaurant(df):

    return (
        df.groupby("restaurant")
        .size()
        .reset_index(name="Dish Count")
        .sort_values("Dish Count", ascending=False)
    )


# =====================================================
# AVERAGE PRICE PER CUISINE
# =====================================================

def average_price_cuisine(df):

    return (
        df.groupby("cuisine_type")["price"]
        .mean()
        .reset_index()
        .sort_values("price", ascending=False)
    )


# =====================================================
# DISH TYPE COUNTS
# =====================================================

def dish_type_counts(df):

    if "dish_type" not in df.columns:
        return pd.DataFrame()

    return (
        df.groupby("dish_type")
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )


# =====================================================
# FOOD TYPE COUNTS
# =====================================================

def food_type_counts(df):

    if "food_type" not in df.columns:
        return pd.DataFrame()

    return (
        df.groupby("food_type")
        .size()
        .reset_index(name="Count")
    )


# =====================================================
# TOP INGREDIENTS
# =====================================================

def top_ingredients(df, top_n=15):

    if "main_ingredients" not in df.columns:
        return pd.DataFrame()

    ingredient_list = []

    for ingredients in df["main_ingredients"]:

        # Skip missing values
        if ingredients is None:
            continue

        # If stored as string (loaded from CSV)
        if isinstance(ingredients, str):

            ingredients = ingredients.strip()

            if ingredients == "":
                continue

            try:
                import ast
                ingredients = ast.literal_eval(ingredients)
            except Exception:
                ingredients = [x.strip() for x in ingredients.split(",")]

        # If already a list
        if isinstance(ingredients, list):

            ingredient_list.extend(
                [x.strip().lower() for x in ingredients if x]
            )

    ingredient_df = (
        pd.Series(ingredient_list)
        .value_counts()
        .head(top_n)
        .reset_index()
    )

    ingredient_df.columns = ["Ingredient", "Count"]

    return ingredient_df

# =====================================================
# MOST EXPENSIVE DISHES
# =====================================================

def expensive_dishes(df, top_n=10):

    return (
        df.sort_values("price", ascending=False)
        [["dish_name", "restaurant", "price"]]
        .head(top_n)
    )


# =====================================================
# CHEAPEST DISHES
# =====================================================

def cheapest_dishes(df, top_n=10):

    return (
        df.sort_values("price")
        [["dish_name", "restaurant", "price"]]
        .head(top_n)
    )


# =====================================================
# RESTAURANT MENU SIZE
# =====================================================

def menu_size(df):

    return (
        df.groupby("restaurant")
        .size()
        .reset_index(name="Total Dishes")
        .sort_values("Total Dishes", ascending=False)
    )


# =====================================================
# PRICE BY FOOD TYPE
# =====================================================

def average_price_food_type(df):

    if "food_type" not in df.columns:
        return pd.DataFrame()

    return (
        df.groupby("food_type")["price"]
        .mean()
        .reset_index()
    )


# =====================================================
# PRICE BY DISH TYPE
# =====================================================

def average_price_dish_type(df):

    if "dish_type" not in df.columns:
        return pd.DataFrame()

    return (
        df.groupby("dish_type")["price"]
        .mean()
        .reset_index()
        .sort_values("price", ascending=False)
    )


# =====================================================
# PRICE SUMMARY
# =====================================================

def price_summary(df):

    return df["price"].describe()


# =====================================================
# COMPLETE ANALYSIS
# =====================================================

def run_analysis(df):

    results = {

        "basic_stats": get_basic_statistics(df),

        "avg_price_restaurant": average_price_restaurant(df),

        "dish_count": dish_count_restaurant(df),

        "avg_price_cuisine": average_price_cuisine(df),

        "dish_type_count": dish_type_counts(df),

        "food_type_count": food_type_counts(df),

        "top_ingredients": top_ingredients(df),

        "expensive_dishes": expensive_dishes(df),

        "cheap_dishes": cheapest_dishes(df),

        "menu_size": menu_size(df),

        "avg_food_price": average_price_food_type(df),

        "avg_dish_price": average_price_dish_type(df),

        "price_summary": price_summary(df)

    }

    return results


# =====================================================
# TESTING
# =====================================================

if __name__ == "__main__":

    from Data_loader import load_data
    from ingredient_extractor import create_features

    df = load_data()

    df = create_features(df)

    analysis = run_analysis(df)

    print("\nBasic Statistics")
    print(analysis["basic_stats"])

    print("\nAverage Price Per Restaurant")
    print(analysis["avg_price_restaurant"])

    print("\nTop Ingredients")
    print(analysis["top_ingredients"])

    print("\nMost Expensive Dishes")
    print(analysis["expensive_dishes"])