# src/ui/_streamlit/entry.py
import streamlit as st

# Define both pages pointing cleanly to individual string file paths
home_page = st.Page(
    "src/ui/_streamlit/entry_home.py",  # <-- Points to the new homepage file
    title="Home", 
    url_path="home", 
    default=True
)

character_page = st.Page(
    "src/ui/_streamlit/entry_char.py",  # <-- Points to your workspace file
    title="Character Hub", 
    url_path="character"
)

# This function remains exactly what your main root file (streamlit_app.py) runs
def render():
    pg = st.navigation([home_page, character_page], position="hidden")
    pg.run()
