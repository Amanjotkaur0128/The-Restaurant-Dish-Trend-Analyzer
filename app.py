import streamlit as st
import pandas as pd

# Import project modules
from Data_loader import load_data
from ingredient_extractor import create_features
from trend_analysis import run_analysis
from visualization import *

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="The Evolving Menu",
    layout="wide"
)
# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* ===============================
   MAIN BACKGROUND
================================ */

.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b,#334155);
    color:white;
}

/* ===============================
   HIDE STREAMLIT DEFAULTS
================================ */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* ===============================
   SIDEBAR
================================ */

section[data-testid="stSidebar"]{
    background:#020617;
}

section[data-testid="stSidebar"] *{
    color:white;
}

/* ===============================
   TITLE
================================ */

.main-title{
    font-size:50px;
    font-weight:900;
    color:#38bdf8;
    text-align:center;
}

.subtitle{
    text-align:center;
    font-size:20px;
    color:#cbd5e1;
    margin-bottom:30px;
}

/* ===============================
   METRIC CARDS
================================ */

.metric-card{

    background:#1e293b;

    border-radius:18px;

    padding:25px;

    text-align:center;

    color:white;

    border:1px solid #334155;

    box-shadow:0px 5px 20px rgba(0,0,0,.45);

    transition:.3s;

}

.metric-card:hover{

    transform:translateY(-6px);

    border:1px solid #38bdf8;

}

/* ===============================
   SECTION TITLES
================================ */

.section-title{

    font-size:28px;

    font-weight:bold;

    color:#38bdf8;

    padding-top:20px;

    padding-bottom:10px;

}

/* ===============================
   BUTTONS
================================ */

.stButton>button{

    background:#0ea5e9;

    color:white;

    border:none;

    border-radius:10px;

    font-weight:bold;

}

.stButton>button:hover{

    background:#0284c7;

}

/* ===============================
   DOWNLOAD BUTTON
================================ */

.stDownloadButton>button{

    background:#22c55e;

    color:white;

    border:none;

    border-radius:10px;

}

/* ===============================
   DATAFRAME
================================ */

div[data-testid="stDataFrame"]{

    border:2px solid #334155;

    border-radius:12px;

}

/* ===============================
   PLOTLY CHARTS
================================ */

div[data-testid="stPlotlyChart"]{

    border-radius:15px;

    border:1px solid #334155;

    padding:10px;

    background:#0f172a;

}

/* ===============================
   SCROLL BAR
================================ */

::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:#38bdf8;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

st.title("The Evolving Menu")
st.subheader("Restaurant Dish Trend Analyzer")

st.markdown("---")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = load_data()

if df.empty:
    st.error("No data found.")
    st.stop()

# --------------------------------------------------
# FEATURE ENGINEERING
# --------------------------------------------------

df = create_features(df)

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

analysis = run_analysis(df)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("Filters")

# Restaurant
restaurant = st.sidebar.selectbox(
    "Restaurant",
    ["All"] + sorted(df["restaurant"].unique())
)


# Food Type
food = st.sidebar.selectbox(
    "Food Type",
    ["All", "Veg", "Non-Veg"]
)

# Dish Type
dish = st.sidebar.selectbox(
    "Dish Type",
    ["All"] + sorted(df["dish_type"].unique())
)

# Price
price = st.sidebar.slider(
    "Price",
    int(df.price.min()),
    int(df.price.max()),
    (
        int(df.price.min()),
        int(df.price.max())
    )
)

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered = df.copy()

if restaurant != "All":
    filtered = filtered[
        filtered["restaurant"] == restaurant
    ]

if food != "All":
    filtered = filtered[
        filtered["food_type"] == food
    ]

if dish != "All":
    filtered = filtered[
        filtered["dish_type"] == dish
    ]

filtered = filtered[
    (filtered["price"] >= price[0]) &
    (filtered["price"] <= price[1])
]

# --------------------------------------------------
# RUN ANALYSIS AGAIN ON FILTERED DATA
# --------------------------------------------------

analysis = run_analysis(filtered)

# --------------------------------------------------
# METRICS
# --------------------------------------------------

st.header("Dashboard Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Restaurants",
    filtered["restaurant"].nunique()
)

col2.metric(
    "Total Dishes",
    len(filtered)
)

col3.metric(
    "Average Price",
    f"${filtered['price'].mean():.2f}"
)

col4.metric(
    "Highest Price",
    f"${filtered['price'].max():.2f}"
)

st.markdown("---")

# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------

st.header("Dataset")

df = pd.read_csv("data/cleaned_featured_menu_data.csv")

st.dataframe(df, use_container_width=True)

st.markdown("---")

# --------------------------------------------------
# VISUALIZATIONS
# --------------------------------------------------

st.header("Restaurant Analysis")

st.plotly_chart(
    plot_average_price_restaurant(
        analysis["avg_price_restaurant"]
    ),
    use_container_width=True
)

st.plotly_chart(
    plot_dish_count(
        analysis["dish_count"]
    ),
    use_container_width=True
)

st.plotly_chart(
    plot_price_distribution(filtered),
    use_container_width=True
)

st.plotly_chart(
    plot_boxplot(filtered),
    use_container_width=True
)

st.markdown("---")

# --------------------------------------------------
# CUISINE ANALYSIS
# --------------------------------------------------

st.header("Cuisine Analysis")

st.plotly_chart(
    plot_cuisine_prices(
        analysis["avg_price_cuisine"]
    ),
    use_container_width=True
)

# --------------------------------------------------
# INGREDIENT ANALYSIS
# --------------------------------------------------

st.header("Ingredient Analysis")

if not analysis["top_ingredients"].empty:

    st.plotly_chart(
        plot_top_ingredients(
            analysis["top_ingredients"]
        ),
        use_container_width=True
    )

fig = create_wordcloud(filtered)

st.markdown("---")

# --------------------------------------------------
# FOOD TYPE
# --------------------------------------------------

st.header("Food Type")

if not analysis["food_type_count"].empty:

    st.plotly_chart(
        plot_food_types(
            analysis["food_type_count"]
        ),
        use_container_width=True
    )

# --------------------------------------------------
# DISH TYPE
# --------------------------------------------------

st.header("Dish Types")

if not analysis["dish_type_count"].empty:

    st.plotly_chart(
        plot_dish_types(
            analysis["dish_type_count"]
        ),
        use_container_width=True
    )

# --------------------------------------------------
# SCATTER
# --------------------------------------------------

st.header("Ingredient Count vs Price")

st.plotly_chart(
    plot_scatter(filtered),
    use_container_width=True
)

# --------------------------------------------------
# MENU SIZE
# --------------------------------------------------

st.header("Restaurant Menu Size")

st.plotly_chart(
    plot_menu_size(
        analysis["menu_size"]
    ),
    use_container_width=True
)

# --------------------------------------------------
# EXPENSIVE DISHES
# --------------------------------------------------

st.header("Most Expensive Dishes")

st.dataframe(
    analysis["expensive_dishes"],
    use_container_width=True
)

st.plotly_chart(
    plot_expensive_dishes(
        analysis["expensive_dishes"]
    ),
    use_container_width=True
)

# --------------------------------------------------
# CHEAPEST DISHES
# --------------------------------------------------

st.header("Cheapest Dishes")

st.dataframe(
    analysis["cheap_dishes"],
    use_container_width=True
)

st.plotly_chart(
    plot_cheapest_dishes(
        analysis["cheap_dishes"]
    ),
    use_container_width=True
)

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

st.markdown("---")

st.download_button(
    label="Download Filtered Dataset",
    data=filtered.to_csv(index=False),
    file_name="filtered_menu_data.csv",
    mime="text/csv"
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "The Evolving Menu • Restaurant Dish Trend Analyzer • Built with Streamlit & Plotly"
)