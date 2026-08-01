import streamlit as st

from dashboard_utils import get_filtered_data
from trend_analysis import run_analysis
from visualization import plot_average_price_restaurant, plot_cuisine_prices, plot_dish_count, plot_menu_size

st.title("Overview")

filtered = get_filtered_data()
analysis = run_analysis(filtered)

one, two, three, four = st.columns(4)
one.metric("Restaurants", filtered["restaurant"].nunique())
two.metric("Dishes", len(filtered))
three.metric("Average price", f"{filtered['price'].mean():,.0f}")
four.metric("Highest price", f"{filtered['price'].max():,.0f}")

left, right = st.columns(2)
with left:
    st.plotly_chart(plot_average_price_restaurant(analysis["avg_price_restaurant"]), use_container_width=True)
with right:
    st.plotly_chart(plot_dish_count(analysis["dish_count"]), use_container_width=True)

left, right = st.columns(2)
with left:
    st.plotly_chart(plot_cuisine_prices(analysis["avg_price_cuisine"]), use_container_width=True)
with right:
    st.plotly_chart(plot_menu_size(analysis["menu_size"]), use_container_width=True)
