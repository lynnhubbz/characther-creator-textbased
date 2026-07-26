# entry.py
import streamlit as st

from .sidebar import *
from .characthercreator import *
from .files.jsonviewer import *


def render():
    # 1. Render the sidebar
    render_sidebar()

    # 2. Get current active page from session_state
    current_page = st.session_state.get("current_page", "Intro")

    # 3. Render Main Content based on selection
    st.title(f"📍 {current_page}")

    if current_page == "Intro":
        st.write("Welcome to the application!")

    elif current_page == "Settings":
        st.write("Configure your settings here.")

    elif current_page == "Character Editor":
        render_characthereditor()

    elif current_page == "Export":
        render_jsonviewer()

    elif current_page == "Import":
        st.write("Import Panel")