import streamlit as st

st.set_page_config(initial_sidebar_state="locked")
sidebar = st.sidebar

sidebar.header("Navigation")

homemenu = sidebar.container(
    border=True,
)
homemenu.header("Home")

intro_button = homemenu.button(
    label="Intro",
    use_container_width=True
)

intro_button = homemenu.button(
    label="",
    use_container_width=True
)

toolmenu = sidebar.container(
    border=True
)
toolmenu.header("Tool")

setting_button = toolmenu.button(
    label="Settings",
    use_container_width=True
)

char_menu = sidebar.container(
    border=True
)
char_menu.header("Characther")

char_button = char_menu.button(
    label="test",
    use_container_width=True
)

filesmenu = sidebar.container(
    border=True
)
filesmenu.header("Files")

export_button = filesmenu.button(
    label="Export",
    use_container_width=True
)

import_button = filesmenu.button(
    label="Import",
    use_container_width=True
)