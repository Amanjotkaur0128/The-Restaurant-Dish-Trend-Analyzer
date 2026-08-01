import streamlit as st

from dashboard_utils import get_filtered_data
from trend_analysis import run_analysis
from visualization import plot_boxplot, plot_expensive_dishes, plot_price_distribution, plot_scatter,plot_cheapest_dishes

st.title("Pricing")

filtered = get_filtered_data()
analysis = run_analysis(filtered)

left, right = st.columns(2)
with left:
    st.plotly_chart(plot_price_distribution(filtered), use_container_width=True)
with right:
    st.plotly_chart(plot_boxplot(filtered), use_container_width=True)

st.plotly_chart(plot_scatter(filtered), use_container_width=True)

left, right = st.columns(2)
with left:
    st.plotly_chart(plot_expensive_dishes(analysis["expensive_dishes"]), use_container_width=True)
with right:
    st.subheader("Most expensive dishes")
    st.dataframe(analysis["expensive_dishes"], use_container_width=True, hide_index=True)

left, right = st.columns(2)
with left:
    st.plotly_chart(plot_cheapest_dishes(analysis["cheap_dishes"]),use_container_width=True,)
with right:
    st.subheader("Cheapest dishes in menu")
    st.dataframe(analysis["cheap_dishes"], use_container_width = True, hide_index = True,)