# entry.py
import streamlit as st

from .sidebar import *
from .characthercreator import *
from .files.jsonviewer import *
from .utils import *




def render():
    # 1. Render the sidebar
    render_sidebar()

    # 2. Get current active page from session_state
    current_page = st.session_state.get("current_page", "Intro")

    # 3. Render Main Content based on selection
    st.title(f"🎼 {current_page}")


    if current_page == "Intro":
        st.caption("Welcome to the application!")
        st.markdown(read_markdown_file("README.md"))

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

# @todo second column for informations