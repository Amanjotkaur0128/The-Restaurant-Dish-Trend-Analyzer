import pandas as pd
import re
import os
import streamlit as st # Import st for caching and error messages

# Define the relative path to the CSV file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(
    BASE_DIR,
    "data",
    "cleaned_featured_menu_data.csv"
)


def clean_price(price_input):
    """
    Cleans a price input (can be string or numeric) into a float.
    Handles NaN values and applies sanity checks.
    """
    if pd.isna(price_input):
        return None

    if isinstance(price_input, (int, float)):
        if 100 <= price_input <= 100000: # Adjust bounds if needed
            return price_input
        else:
            return None

    price_str = str(price_input)
    cleaned_price = re.sub(r'[^\d.]', '', price_str).strip()

    if not cleaned_price or cleaned_price == '.':
        return None
    try:
        price_float = float(cleaned_price)
        if 100 <= price_float <= 100000:
            return price_float
        else:
            return None
    except ValueError:
        return None

@st.cache_data
def load_data():
    """
    Loads and preprocesses the menu data from the CSV file.
    Uses Streamlit's cache_data to avoid reloading on every rerun.
    """
    if not os.path.exists(CSV_PATH):
        st.error(f"Error: CSV file not found at {CSV_PATH}. Please ensure 'cleaned_menu_data.csv' is in the 'data' folder.")
        return pd.DataFrame()
    try:
        df = pd.read_csv(CSV_PATH)
        if 'price' in df.columns:
            df['price'] = df['price'].apply(clean_price)
            df.dropna(subset=['price'], inplace=True)
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            df.dropna(subset=['price'], inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading data from {CSV_PATH}: {e}")
        return pd.DataFrame()

# You can also define other utility functions here if needed
