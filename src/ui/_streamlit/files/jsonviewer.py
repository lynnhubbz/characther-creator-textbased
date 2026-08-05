from enum import Enum
from typing import Any, Dict, Literal, Optional, Tuple, get_args, get_origin
import streamlit as st
from pydantic import BaseModel, Field

from ..characthercreator import *
from ....core.filemanager import *

jsonindent = 4

def render_exportpage():
    char = st.session_state.character
    assets_dict = st.session_state.get("pending_assets", {})

    json_str = char.model_dump_json(indent=4)
    zip_bytes = create_character_bundle(
        character_json=json_str,
        assets=assets_dict
    )

    st.caption("Saved file will contain direct key-value mapping with `null` defaults.")

    col1, col2 = st.columns([3, 2], border=True)

    with col2:
        st.header("Downloads")
        st.download_button(
            label="💾 Download Character JSON",
            data=json_str,
            file_name="character.json",
            mime="application/json",
            use_container_width=True
        )

        st.download_button(
            label="Download .zip Bundle",
            data=zip_bytes,
            file_name=f"{char.CHARACTER_GENERAL.Names.full_name or 'character'}_bundle.zip",
            mime="application/zip",
            use_container_width=True
        )

        st.subheader("Settings")

    with col1:
        st.header("Previews")
        st.subheader("Directory Map Preview")
        tree_lines = generate_directory_preview(list(assets_dict.keys()))
        st.code("\n".join(tree_lines), language="text")

        st.subheader("📄 Live Exported JSON")
        st.code(json_str, language="json")