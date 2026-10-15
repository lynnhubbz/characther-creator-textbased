# src/ui/_streamlit/entry_home.py
import streamlit as st
from src.ui._streamlit.utils import read_markdown_file

st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

st.title("🎼 TexTBase", text_alignment="center")
st.caption("Welcome to the application! Select a workspace below to get started.", text_alignment="center")
st.write("---")

# 1. Inject subtle CSS to style native containers into premium interactive cards
st.markdown("""
    <style>
    /* Style the outer metric/workspace card containers */
    div[data-testid="stVBlockBorder"] {
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Add an elegant lift and glow effect on hover */
    div[data-testid="stVBlockBorder"]:hover {
        transform: translateY(-4px);
        border-color: #cbd5e1 !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04) !important;
    }

    /* Style the main Action Button inside the card */
    div[data-testid="stVBlockBorder"] button {
        background-color: #4f46e5 !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: background-color 0.2s ease !important;
    }
    
    div[data-testid="stVBlockBorder"] button:hover {
        background-color: #4338ca !important;
    }
    </style>
""", unsafe_allow_html=True)
# src/ui/_streamlit/entry_home.py

side_margin = 0.20
card_width = 0.30

columns_layout = [side_margin, card_width, card_width, side_margin]
left_pad, col1, col2, right_pad = st.columns(columns_layout)

# 2. Place your workspace cards in the centered layout slots
with col1:
    with st.container(border=True):
        st.markdown("### 👤 Character Creator")
        st.write("Manage general details, tweak appearance styles, and import/export configurations.")
        if st.button("Enter Workspace →", key="go_to_char"):
            st.switch_page("src/ui/_streamlit/entry_char.py")

with col2:
    with st.container(border=True):
        st.markdown("### 🧬 Race Creator")
        st.write("Configure distinct lineage stats, mechanical traits, and unique cultural modifiers.")
        if st.button("Enter Workspace →", key="go_to_race"):
            st.switch_page("src/ui/_streamlit/entry_race.py")

st.divider()

# 3. Restrain your README text body so it matches the width of the cards perfectly
text_layout = [side_margin, 0.60, side_margin]
text_left, text_content, text_right = st.columns(text_layout)

with text_content:
    st.markdown(read_markdown_file("README.md"))
