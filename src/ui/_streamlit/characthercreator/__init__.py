from enum import Enum
from typing import Any, Dict, Literal, Optional, Tuple, get_args, get_origin
import streamlit as st
from pydantic import BaseModel, Field

from ....core import base
from .widgets import *

# Initialize session state for character data
if "character" not in st.session_state:
    st.session_state.character = base.CharacterData()

# Store uploaded asset bytes in session state for export
if "pending_assets" not in st.session_state:
    st.session_state.pending_assets = {}

char: base.CharacterData = st.session_state.character



# --- 5. Main Streamlit Application ---
def _auto_render(sections):
    '''
    Assuming `sections` are a list of tuples, which the tuple contains title, section, and unique key
    '''
    for title, section_obj, key, *skip_nested in sections:
        
        skip_nested = skip_nested[0] if skip_nested else True
        
        st.header(title)
        
        col1, col2 = st.columns([5, 3], border=True)
        with col1:
            # Render the section UI using the direct object
            updates = render_pydantic_section(section_obj, key, skip_nested=skip_nested)
            
            # Update the object IN-PLACE. 
            # Because section_obj points directly to char.CHARACTER_IDENTITY.X in memory,
            # modifying it here automatically updates the main `char` object!
            for field_name, new_value in updates.items():
                setattr(section_obj, field_name, new_value)

def render_characteridentity():

    st.caption("lorem ipsum dolor sit amet")

    st.divider()
    
    sections = [
        ("👤 Names", char.CHARACTER_IDENTITY.Names, "names"),
        ("⚧ Gender & Sexuality", char.CHARACTER_IDENTITY.Gender_and_Sex, "gender_sex"),
        ("💼 Occupation & Details", char.CHARACTER_IDENTITY.Occupational, "occupational"),
    ]
    _auto_render(sections)

def render_characterappearance():
    st.caption("lorem ipsum dolor sit amet")

    st.divider()

    sections = [
        # (Title, Object, Key, Skip Nested Models?)
        ("👤 RefSheet", char.CHARACTER_APPEARANCE, "character_appearance", True),  # <-- Only renders refsheet_link
        ("💼 General Body", char.CHARACTER_APPEARANCE.General_Body, "General_Body", False), # <-- Renders General_Body + Age
    ]

    _auto_render(sections)
