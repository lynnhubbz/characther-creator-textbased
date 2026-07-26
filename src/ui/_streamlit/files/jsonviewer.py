from enum import Enum
from typing import Any, Dict, Literal, Optional, Tuple, get_args, get_origin
import streamlit as st
from pydantic import BaseModel, Field

from ..characthercreator import *

def render_jsonviewer():
    st.subheader("📄 Live Exported JSON")
    st.caption("Saved file will contain direct key-value mapping with `null` defaults.")

    json_str = char.model_dump_json(indent=2)
    st.code(json_str, language="json")

    st.download_button(
        label="💾 Download Character JSON",
        data=json_str,
        file_name="character.json",
        mime="application/json",
    )