# src/ui/_streamlit/entry_char.py
import streamlit as st

from src.ui._streamlit.character import *
from src.ui._streamlit.files.jsonviewer import *
from src.ui._streamlit.character.sidebar import *
from src.ui._streamlit.utils import *
# Inside src/ui/_streamlit/entry_char.py

st.set_page_config(initial_sidebar_state="locked", layout="wide")

def render():
    with st.sidebar:
        # CHANGE THIS TO THE EXACT FILE PATH STRING:
        if st.button("⬅ Exit Workspace", use_container_width=True):
            st.switch_page("src/ui/_streamlit/entry_home.py") # <-- Exact path from project root
        st.write("---")

        
    render_sidebar()
    current_page = st.session_state.get("current_page", "Intro")
    st.title(f"🎼 {current_page}")

    if current_page == "Intro":
        st.caption("Welcome to the application!")
    elif current_page == "Settings":
        st.write("Configure your settings here.")
    elif current_page == "General":
        render_charactergeneral()
    elif current_page == "Appearance":
        render_characterappearance()
    elif current_page == "Export":
        render_exportpage()
    elif current_page == "Import":
        st.write("Import Panel")

render()
