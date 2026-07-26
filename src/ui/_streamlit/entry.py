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

    elif current_page == "Identity":
        render_characteridentity()

    elif current_page == "Appearance":
        render_characterappearance()

    elif current_page == "Export":
        col1, col2 = st.columns(2)

        with col1:
            render_jsonviewer()
        with col2:
            render_export_page()

    elif current_page == "Import":
        st.write("Import Panel")