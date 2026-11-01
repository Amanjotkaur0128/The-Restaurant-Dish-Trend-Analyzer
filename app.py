import streamlit as st

from dashboard_utils import get_menu_data

st.set_page_config(page_title="The Restaurant Dish Trend Analyzer", layout="wide")

PROJECT_TECHNOLOGIES = [
    "Python", "Streamlit", "Pandas", "NumPy", "Plotly", "Beautiful Soup",
    "Requests", "Regular Expressions", "Matplotlib", "WordCloud",
]
DEVELOPERS = ["Amanjot Kaur", "Tarannum"]
DATASET_FILE = "data/cleaned_featured_menu_data.csv"

st.markdown(
    """
    <style>
        .stApp { background: #f7f4ef; color: #172a3a; }
        [data-testid="stHeader"] { background: rgba(0, 0, 0, 0); }

        
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #172a3a 0%, #0d1b2a 100%); }
[data-testid="stSidebar"] * { color: #f8f4eb; }
        [data-testid="stSidebarNav"] a,
        [data-testid="stSidebarNav"] a span { color: #f8f4eb !important; opacity: 1 !important; font-weight: 600; }
        [data-testid="stSidebarNav"] a:hover { background: #315468 !important; color: #ffffff !important; border-radius: 8px; }
        [data-testid="stSidebarNav"] a[aria-current="page"] { background: #f2dfc4 !important; border-radius: 8px; }
        [data-testid="stSidebarNav"] a[aria-current="page"],
        [data-testid="stSidebarNav"] a[aria-current="page"] span { color: #172a3a !important; font-weight: 800 !important; }

        /* All sidebar text stays light */
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] a,
        [data-testid="stSidebar"] button,
        [data-testid="stSidebar"] [role="button"] {
            color: #ffffff !important;
            opacity: 1 !important;
        }

        .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3 { color: #172a3a; }
        .hero-card { background: linear-gradient(115deg, #172a3a 0%, #274c5e 68%, #9c5c2b 100%); border-radius: 22px; padding: 2.2rem 2.5rem; color: #ffffff; margin: 0.5rem 0 1.5rem 0; box-shadow: 0 12px 28px rgba(23,42,58,.18); }
        .hero-card h1 { color: #ffffff; font-size: 2.6rem; margin: 0; }
        .hero-card p { color: #e6edf0; font-size: 1.05rem; margin: .6rem 0 0; }
        .section-label { color: #9c5c2b; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: .78rem; }
        .technology-chip { display: inline-block; padding: .45rem .7rem; margin: .25rem .2rem .25rem 0; border-radius: 999px; background: #e3ece8; color: #173d42; font-size: .85rem; font-weight: 600; }
        .credit-card { background: #ffffff; border-left: 5px solid #c78842; border-radius: 12px; padding: 1rem; box-shadow: 0 4px 14px rgba(23,42,58,.08); }
        [data-testid="stMetric"] { background: #ffffff; border: 1px solid #e6ded2; border-radius: 14px; padding: 1rem; box-shadow: 0 4px 14px rgba(23,42,58,.06); }
        .stButton > button, .stDownloadButton > button { background: #a9602d; color: #ffffff; border: 0; border-radius: 9px; font-weight: 600; }
        .stButton > button:hover, .stDownloadButton > button:hover { background: #7d451f; color: #ffffff; }
        div[data-testid="stExpander"] { background: #ffffff; border: 1px solid #e6ded2; border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)


def menu_assistant_reply(question):
    """Answer common menu questions using the project dataset."""
    data = get_menu_data()
    query = question.lower()

    if "price" in query or "cost" in query or "expensive" in query:
        highest = data.loc[data["price"].idxmax()]
        return f"The average menu price is {data['price'].mean():,.0f}. The most expensive dish is {highest['dish_name']} at {highest['price']:,.0f}."
    if "restaurant" in query:
        counts = data["restaurant"].value_counts()
        return f"The dataset has {len(counts)} restaurants. {counts.index[0]} has the largest menu with {counts.iloc[0]} dishes."
    if "veg" in query or "vegetarian" in query:
        vegetarian = (data["food_type"] == "Veg").sum()
        return f"There are {vegetarian} vegetarian dishes out of {len(data)} menu items."
    if "ingredient" in query or "popular" in query or "top" in query:
        ingredients = data["ingredients"].fillna("").str.split(",").explode().str.strip()
        top = ingredients[ingredients.ne("")].value_counts().head(3)
        return "The most common extracted ingredients are " + ", ".join(f"{name} ({count})" for name, count in top.items()) + "."
    return "Try asking about prices, restaurants, vegetarian dishes, or popular ingredients."


def render_chatbot():
    with st.sidebar:
        st.divider()
        st.markdown(
            "<h3 style='color: white;'>Menu Assistant</h3>",
            unsafe_allow_html=True
        )
        st.caption("Ask about prices, restaurants, vegetarian dishes, or ingredients.")
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        question = st.chat_input("Ask about the menu", key="menu_assistant_input")
        if question:
            st.session_state.chat_messages.extend([
                {"role": "user", "content": question},
                {"role": "assistant", "content": menu_assistant_reply(question)},
            ])
            st.rerun()
        if st.button("Clear chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()


pages = [
    st.Page("pages/1.Home.py", title="Home"),
    st.Page("pages/2.Overview.py", title="Overview"),
    st.Page("pages/3.dataset.py", title="Dataset"),
    st.Page("pages/4.Ingredients&dishes.py", title="Ingredients & dishes"),
    st.Page("pages/5.Pricing.py", title="Pricing"),
]

selected_page = st.navigation(pages, position="sidebar")
render_chatbot()
selected_page.run()
