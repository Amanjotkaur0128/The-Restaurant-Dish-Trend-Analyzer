import streamlit as st

from dashboard_utils import get_filtered_data

st.title("Dataset explorer")

filtered = get_filtered_data()
st.caption(f"{len(filtered)} dishes match the current filters.")
st.dataframe(filtered, use_container_width=True, hide_index=True)
st.download_button(
    "Download filtered data",
    filtered.to_csv(index=False),
    file_name="filtered_menu_data.csv",
    mime="text/csv",
)
