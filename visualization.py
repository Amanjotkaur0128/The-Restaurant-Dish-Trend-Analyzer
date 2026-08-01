import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

px.defaults.color_discrete_sequence = ["#a9602d", "#1f6f78", "#d79a43", "#5e8b7e", "#9b4f96", "#455a8a"]
px.defaults.color_continuous_scale = ["#f4ddc3", "#d79a43", "#a9602d"]


# ==========================================================
# Average Price by Restaurant
# ==========================================================

def plot_average_price_restaurant(df):

    fig = px.bar(
        df,
        x="restaurant",
        y="price",
        color="price",
        title="Average Dish Price by Restaurant",
        text_auto=".2f"
    )

    fig.update_layout(
        xaxis_title="Restaurant",
        yaxis_title="Average Price",
        template="simple_white"
    )

    return fig


# ==========================================================
# Number of Dishes
# ==========================================================

def plot_dish_count(df):

    fig = px.bar(
        df,
        x="restaurant",
        y="Dish Count",
        color="Dish Count",
        title="Number of Dishes per Restaurant",
        text_auto=True
    )

    fig.update_layout(template="simple_white")

    return fig


# ==========================================================
# Price Histogram
# ==========================================================

def plot_price_distribution(df):

    fig = px.histogram(
        df,
        x="price",
        nbins=20,
        color_discrete_sequence=["#a9602d"],
        title="Price Distribution"
    )

    fig.update_layout(template="simple_white")

    return fig


# ==========================================================
# Box Plot
# ==========================================================

def plot_boxplot(df):

    fig = px.box(
        df,
        x="restaurant",
        y="price",
        color="restaurant",
        title="Restaurant Price Comparison"
    )

    fig.update_layout(template="simple_white")

    return fig


# ==========================================================
# Top Ingredients
# ==========================================================

def plot_top_ingredients(df):

    fig = px.bar(
        df,
        x="Ingredient",
        y="Count",
        color="Count",
        title="Top Ingredients",
        text_auto=True
    )

    fig.update_layout(template="simple_white")

    return fig


# ==========================================================
# Dish Types
# ==========================================================

def plot_dish_types(df):

    fig = px.pie(
        df,
        names="dish_type",
        values="Count",
        title="Dish Type Distribution"
    )

    return fig


# ==========================================================
# Food Type (Veg / Non-Veg)
# ==========================================================

def plot_food_types(df):

    fig = px.pie(
        df,
        names="food_type",
        values="Count",
        title="Veg vs Non-Veg"
    )

    return fig


# ==========================================================
# Cuisine Prices
# ==========================================================

def plot_cuisine_prices(df):

    fig = px.bar(
        df,
        x="cuisine_type",
        y="price",
        color="price",
        title="Average Price by Cuisine",
        text_auto=".2f"
    )

    fig.update_layout(template="simple_white")

    return fig


# ==========================================================
# Expensive Dishes
# ==========================================================

def plot_expensive_dishes(df):

    fig = px.bar(
        df,
        x="dish_name",
        y="price",
        color="restaurant",
        title="Top Expensive Dishes",
        text_auto=".2f"
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        template="simple_white"
    )

    return fig


# ==========================================================
# Cheapest Dishes
# ==========================================================

def plot_cheapest_dishes(df):

    fig = px.bar(
        df,
        x="dish_name",
        y="price",
        color="restaurant",
        title="Cheapest Dishes",
        text_auto=".2f"
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        template="simple_white"
    )

    return fig


# ==========================================================
# Ingredient Count vs Price
# ==========================================================

def plot_scatter(df):

    fig = px.scatter(
        df,
        x="ingredient_count",
        y="price",
        color="restaurant",
        size="ingredient_count",
        hover_name="dish_name",
        title="Ingredient Count vs Price"
    )

    fig.update_layout(template="simple_white")

    return fig


# ==========================================================
# Word Cloud
# ==========================================================

def create_wordcloud(df):

    if len(df) == 0:
        return None

    text = " ".join(df["dish_name"].astype(str))

    wc = WordCloud(
        width=1200,
        height=600,
        background_color="#fffdf9"
    ).generate(text)

    fig, ax = plt.subplots(figsize=(12,6))

    ax.imshow(wc)

    ax.axis("off")

    return fig


# ==========================================================
# Price Gauge
# ==========================================================

def plot_average_price_gauge(avg_price):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_price,
        title={'text': "Average Dish Price"},
        gauge={
            'axis': {'range': [0, avg_price * 2]},
            'bar': {'color': "darkblue"}
        }
    ))

    return fig


# ==========================================================
# Restaurant Menu Size
# ==========================================================

def plot_menu_size(df):

    fig = px.bar(
        df,
        x="restaurant",
        y="Total Dishes",
        color="Total Dishes",
        title="Restaurant Menu Size",
        text_auto=True
    )

    fig.update_layout(template="simple_white")

    return fig
