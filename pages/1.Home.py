from pathlib import Path

import streamlit as st

DATASET_FILE = "data/cleaned_featured_menu_data.csv"
DEVELOPERS = ["Amanjot Kaur", "Tarannum"]
PROJECT_TECHNOLOGIES = [
    "Python", "Streamlit", "Pandas", "NumPy", "Plotly", "Beautiful Soup",
    "Requests", "Regular Expressions", "Matplotlib", "WordCloud",
]
from dashboard_utils import get_menu_data

HERO_IMAGE = "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1600&q=85"
FOOD_IMAGES = [
    "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?auto=format&fit=crop&w=700&q=80",
    "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?auto=format&fit=crop&w=700&q=80",
    "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=700&q=80",
]

st.markdown("<div class='hero-card'><h1>The Evolving Menu: Restaurant Dish Trend Analyzer</h1><p>Explore restaurant dishes, ingredients at the different pricing in one interactive dashboard.</p></div>", unsafe_allow_html=True)
st.image(HERO_IMAGE, use_container_width=True)

menu_data = get_menu_data()
if menu_data.empty:
    st.error("No menu data could be loaded. Check the data file and try again.")
    st.stop()

first, second, third, fourth = st.columns(4)
first.metric("Restaurants", menu_data["restaurant"].nunique())
second.metric("Menu items", len(menu_data))
third.metric("Cuisines", menu_data["cuisine_type"].nunique())
fourth.metric("Average price", f"{menu_data['price'].mean():,.0f}")

left, right = st.columns([1.4, 1])
with left:
    st.markdown("<div class='section-label'>Technology stack</div>", unsafe_allow_html=True)
    chips = "".join(f"<span class='technology-chip'>{item}</span>" for item in PROJECT_TECHNOLOGIES)
    st.markdown(chips, unsafe_allow_html=True)
with right:
    st.markdown("<div class='section-label'>Developed by</div>", unsafe_allow_html=True)
    for developer in DEVELOPERS:
        st.markdown(f"<div class='credit-card'><strong>{developer}</strong><br><span>Project Developer</span></div>", unsafe_allow_html=True)

st.markdown("### Download project dataset")
dataset_path = Path(__file__).resolve().parents[1] / DATASET_FILE
st.download_button(
    "Download cleaned menu dataset (CSV)",
    data=dataset_path.read_bytes(),
    file_name="cleaned_featured_menu_data.csv",
    mime="text/csv",
)

st.markdown("### A taste of the menu story")
image_columns = st.columns(3)
for column, image_url in zip(image_columns, FOOD_IMAGES):
    with column:
        st.image(image_url, use_container_width=True)

st.info("Use the sidebar to explore the dashboard pages, apply filters, or ask the Menu Assistant.")

