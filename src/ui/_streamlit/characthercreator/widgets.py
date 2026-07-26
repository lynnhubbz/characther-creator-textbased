from enum import Enum
from typing import Any, Dict, Literal, Optional, Tuple, get_args, get_origin
import streamlit as st
from pydantic import BaseModel, Field

from ....api.base import *

def render_pydantic_section(
    section_model: BaseModel, section_key: str
) -> Dict[str, Any]:
    """Dynamically renders Streamlit widgets for any Pydantic model section."""
    updated_values = {}

    for field_name, field_info in type(section_model).model_fields.items():
        current_val = getattr(section_model, field_name)
        label = field_info.description or field_name
        meta = field_info.json_schema_extra or {}
        widget = meta.get("widget")

        unique_key = f"{section_key}_{field_name}"

        # 1. Short Answer -> st.text_input
        # Inside render_pydantic_section:
        if widget == AnswerType.SHORT_ANSWER:
            # If the model field expects a list, format current_val for text input display
            if isinstance(current_val, list):
                display_val = ", ".join(current_val)
            else:
                display_val = str(current_val)

            user_input = st.text_input(label, value=display_val, key=unique_key)

            # Convert comma-separated string back to list if field target type is list
            if field_info.annotation and get_origin(field_info.annotation) is list:
                updated_values[field_name] = [
                    item.strip() for item in user_input.split(",") if item.strip()
                ]
            else:
                updated_values[field_name] = user_input

        # 2. Long Answer -> st.text_area
        elif widget == AnswerType.LONG_ANSWER:
            updated_values[field_name] = st.text_area(
                label, value=current_val, key=unique_key
            )

        # 3. Likert Scale -> st.slider
        # 3. Likert Scale -> st.slider
        elif widget == AnswerType.LIKERT_SCALE:
            # Ensure all values are strictly cast to int so Streamlit overload matches
            min_val: int = int(meta.get("min", 1))
            max_val: int = int(meta.get("max", 5))

            # Fallback to min_val if current_val is None
            slider_val: int = (
                int(current_val) if current_val is not None else min_val
            )

            updated_values[field_name] = st.slider(
                label,
                min_value=min_val,
                max_value=max_val,
                value=slider_val,
                key=unique_key,
            )

        # 4. Multiple Choice -> st.selectbox
        elif widget == AnswerType.MULTIPLE_CHOICE:
            choices = meta.get("choices", [])
            options = ["-- Select --"] + choices

            # Calculate default index
            default_index = 0
            if current_val in choices:
                default_index = options.index(current_val)

            selected = st.selectbox(
                label, options=options, index=default_index, key=unique_key
            )
            updated_values[field_name] = (
                None if selected == "-- Select --" else selected
            )

    return updated_values