import streamlit as st

from Data_loader import load_data
from ingredient_extractor import create_features


@st.cache_data
def get_menu_data():
    return create_features(load_data())


def render_filters(df):
    """Render filters in the page body, keeping the sidebar for navigation and chat."""
    with st.expander("Filter this page", expanded=False):
        first, second, third, fourth = st.columns(4)
        restaurant = first.selectbox(
            "Restaurant", ["All"] + sorted(df["restaurant"].dropna().unique())
        )
        cuisine = second.selectbox(
            "Cuisine", ["All"] + sorted(df["cuisine_type"].dropna().unique())
        )
        food_type = third.selectbox(
            "Food type", ["All"] + sorted(df["food_type"].dropna().unique())
        )
        dish_type = fourth.selectbox(
            "Dish type", ["All"] + sorted(df["dish_type"].dropna().unique())
        )

        minimum, maximum = int(df["price"].min()), int(df["price"].max())
        price_range = st.slider("Price range", minimum, maximum, (minimum, maximum))

    filtered = df.copy()
    if restaurant != "All":
        filtered = filtered[filtered["restaurant"] == restaurant]
    if cuisine != "All":
        filtered = filtered[filtered["cuisine_type"] == cuisine]
    if food_type != "All":
        filtered = filtered[filtered["food_type"] == food_type]
    if dish_type != "All":
        filtered = filtered[filtered["dish_type"] == dish_type]
    return filtered[filtered["price"].between(*price_range)]


def get_filtered_data():
    df = get_menu_data()
    if df.empty:
        st.error("No menu data could be loaded. Check the data file and try again.")
        st.stop()

    filtered = render_filters(df)
    if filtered.empty:
        st.warning("No dishes match the current filters. Widen the page filters and try again.")
        st.stop()
    return filtered
