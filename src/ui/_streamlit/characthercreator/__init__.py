from enum import Enum
from typing import Any, Dict, Literal, Optional, Tuple, get_args, get_origin
import streamlit as st
from pydantic import BaseModel, Field

from .widgets import *

# Initialize session state for character data
if "character" not in st.session_state:
    st.session_state.character = CharacterData()

# Store uploaded asset bytes in session state for export
if "pending_assets" not in st.session_state:
    st.session_state.pending_assets = {}

char: CharacterData = st.session_state.character

# --- 5. Main Streamlit Application ---
def render_characteridentity():
    st.set_page_config(page_title="Character Identity", layout="wide")

    with st.expander("👤 Names", expanded=True):
        name_updates = render_pydantic_section(
            char.CHARACTER_IDENTITY.names, "names"
        )
        char.CHARACTER_IDENTITY.names = NameSection(**name_updates)

    with st.expander("⚧ Gender & Sexuality", expanded=True):
        gender_updates = render_pydantic_section(
            char.CHARACTER_IDENTITY.gender_and_sex, "gender_sex"
        )
        char.CHARACTER_IDENTITY.gender_and_sex = GenderSexSection(
            **gender_updates
        )

    with st.expander("💼 Occupation & Details", expanded=True):
        occ_updates = render_pydantic_section(
            char.CHARACTER_IDENTITY.occupational, "occupational"
        )
        char.CHARACTER_IDENTITY.occupational = OccupationalSection(
            **occ_updates
        )

def render_characterappearance():
    with st.expander("👤 RefSheet", expanded=True):
        appearance_updates = render_pydantic_section(
            char.CHARACTER_APPEARANCE,
            "character_appearance",
        )