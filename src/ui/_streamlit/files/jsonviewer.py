from enum import Enum
from typing import Any, Dict, Literal, Optional, Tuple, get_args, get_origin
import streamlit as st
from pydantic import BaseModel, Field

from ..characthercreator import *
from ....core.filemanager import *

jsonindent = 4

json_str = char.model_dump_json(indent=4)

assets_dict = st.session_state.get("pending_assets", {})

zip_bytes = create_character_bundle(
    character_json=json_str,
    assets=assets_dict
)

def render_exportpage():
    
    st.caption("Saved file will contain direct key-value mapping with `null` defaults.")
    
    col1, col2 = st.columns([2,3], border=True)

    with col1:

        st.header("Downloads")

        st.download_button(
            label="💾 Download Character JSON",
            data=json_str,
            file_name="character.json",
            mime="application/json",
            use_container_width=True
        )

            # 4. Download Button
        st.download_button(
            label="Download .zip Bundle",
            data=zip_bytes,
            file_name=f"{char.CHARACTER_IDENTITY.Names.full_name or 'character'}_bundle.zip",
            mime="application/zip",
            use_container_width=True
        )

        st.subheader("Settings")

    with col2:
        st.header("Previews")

        st.subheader("Directory Map Preview")
        tree_lines = generate_directory_preview(list(assets_dict.keys()))
        st.code("\n".join(tree_lines), language="text")
    
        st.subheader("📄 Live Exported JSON")
        st.code(json_str, language="json")
        
