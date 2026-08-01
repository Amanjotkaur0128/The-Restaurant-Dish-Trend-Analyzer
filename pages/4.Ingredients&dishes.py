import streamlit as st

from dashboard_utils import get_filtered_data
from trend_analysis import run_analysis
from visualization import create_wordcloud, plot_dish_types, plot_food_types, plot_top_ingredients

st.title("Ingredients & dishes")

filtered = get_filtered_data()
analysis = run_analysis(filtered)

left, right = st.columns(2)
with left:
    if analysis["top_ingredients"].empty:
        st.info("No ingredients were identified for the selected dishes.")
    else:
        st.plotly_chart(plot_top_ingredients(analysis["top_ingredients"]), use_container_width=True)
with right:
    st.plotly_chart(plot_dish_types(analysis["dish_type_count"]), use_container_width=True)

left, right = st.columns(2)
with left:
    st.plotly_chart(plot_food_types(analysis["food_type_count"]), use_container_width=True)
with right:
    wordcloud = create_wordcloud(filtered)
    if wordcloud is not None:
        st.pyplot(wordcloud, clear_figure=True)
