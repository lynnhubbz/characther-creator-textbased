from enum import Enum
from typing import Any, Dict, Literal, Optional, Tuple, get_args, get_origin
import streamlit as st
from pydantic import BaseModel, Field

from ..characthercreator import *
from ....core.filemanager import *

jsonindent = 4

def render_jsonviewer():
    st.header("📄 Live Exported JSON")

    json_str = char.model_dump_json(indent=4)

    st.download_button(
        label="💾 Download Character JSON",
        data=json_str,
        file_name="character.json",
        mime="application/json",
        use_container_width=True
    )

    st.caption("Saved file will contain direct key-value mapping with `null` defaults.")


    st.code(json_str, language="json")



def render_export_page():
    st.header("📦 Export Character Package")

        # 1. Get JSON representation from Pydantic
    char_json = char.model_dump_json(indent=4)
    assets_dict = st.session_state.get("pending_assets", {})

        # 3. Generate Zip File in Memory
    zip_bytes = create_character_bundle(
        character_json=char_json,
        assets=assets_dict
    )

    # 4. Download Button
    st.download_button(
        label="Download .zip Bundle",
        data=zip_bytes,
        file_name=f"{char.CHARACTER_IDENTITY.names.full_name or 'character'}_bundle.zip",
        mime="application/zip",
        use_container_width=True
    )

    # 2. Preview ZIP Directory Structure
    st.write("Directory Map Preview")
    tree_lines = generate_directory_preview(list(assets_dict.keys()))
    st.code("\n".join(tree_lines), language="text")



