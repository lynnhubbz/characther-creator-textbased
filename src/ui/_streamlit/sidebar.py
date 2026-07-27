# sidebar.py
from typing import Callable
import streamlit as st


def render_sidebar():
    """Renders the sidebar navigation and updates session_state."""

    # Initialize current_page state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Intro"

    def set_page(page_name: str):
        st.session_state.current_page = page_name

    sidebar = st.sidebar
    sidebar.header("Navigation")

    # --- Home Menu ---
    homemenu = sidebar.container(border=True)
    homemenu.header("Home")
    homemenu.button(
        "Intro",
        icon="ℹ️",
        use_container_width=True,
        on_click=set_page,
        args=("Intro",),
    )

    # --- Tool Menu ---
    toolmenu = sidebar.container(border=True)
    toolmenu.header("Tool")
    toolmenu.button(
        "Settings",
        icon="⚙️",
        use_container_width=True,
        on_click=set_page,
        args=("Settings",),
    )

    # --- Character Menu ---
    char_menu = sidebar.container(border=True)
    char_menu.header("Character")
    char_menu.button(
        "Identity",
        icon="🧙‍♂️",
        use_container_width=True,
        on_click=set_page,
        args=("Identity",),
    )
    char_menu.button(
        "Appearance",
        icon="🧙‍♂️",
        use_container_width=True,
        on_click=set_page,
        args=("Appearance",),
    )

    # --- Files Menu ---
    filesmenu = sidebar.container(border=True)
    filesmenu.header("Files")
    filesmenu.button(
        "Export",
        icon="📥",
        use_container_width=True,
        on_click=set_page,
        args=("Export",),
    )
    filesmenu.button(
        "Import",
        icon="📤",
        use_container_width=True,
        on_click=set_page,
        args=("Import",),
    )