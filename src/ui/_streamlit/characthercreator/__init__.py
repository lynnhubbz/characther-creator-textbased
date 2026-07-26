from enum import Enum
from typing import Any, Dict, Literal, Optional, Tuple, get_args, get_origin
import streamlit as st
from pydantic import BaseModel, Field

from .widgets import *

# Initialize session state for character data
if "character" not in st.session_state:
    st.session_state.character = CharacterData()

char: CharacterData = st.session_state.character

# --- 5. Main Streamlit Application ---
def render_characthereditor():
    st.set_page_config(page_title="Character Creator", layout="wide")

    st.subheader("Edit Character Identity")

    with st.expander("👤 Names", expanded=True):
        name_updates = render_pydantic_section(
            char.character_identity.names, "names"
        )
        char.character_identity.names = NameSection(**name_updates)

    with st.expander("⚧ Gender & Sexuality", expanded=True):
        gender_updates = render_pydantic_section(
            char.character_identity.gender_and_sex, "gender_sex"
        )
        char.character_identity.gender_and_sex = GenderSexSection(
            **gender_updates
        )

    with st.expander("💼 Occupation & Details", expanded=True):
        occ_updates = render_pydantic_section(
            char.character_identity.occupational, "occupational"
        )
        char.character_identity.occupational = OccupationalSection(
            **occ_updates
        )