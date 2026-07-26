import typing
from typing import Any, Dict, Optional

import streamlit as st
from pydantic import BaseModel
from pydantic.fields import FieldInfo

# Assuming AnswerType is imported from your core module
from ....core.base import *


def _is_list_type(annotation: Any) -> bool:
    """Determine if a Pydantic field annotation expects a list."""
    origin = typing.get_origin(annotation)
    return origin is list or annotation is list or origin is typing.List


def _handle_file_upload(section_model: BaseModel, field_name: str, key: str, is_list_type: bool) -> None:
    """Callback triggered only when new files are selected in st.file_uploader."""
    uploaded = st.session_state.get(key)
    if not uploaded:
        return

    # Normalize inputs to lists
    files = uploaded if isinstance(uploaded, list) else [uploaded]
    current = getattr(section_model, field_name) or []
    new_paths = list(current) if isinstance(current, list) else [current]

    # Initialize session state dict if missing
    if "pending_assets" not in st.session_state:
        st.session_state.pending_assets = {}

    for file in files:
        rel_path = f"assets/{file.name}"
        # Store raw asset bytes for ZIP exporter
        st.session_state.pending_assets[rel_path] = file.getvalue()
        if rel_path not in new_paths:
            new_paths.append(rel_path)

    final_val = new_paths if is_list_type else (new_paths[0] if new_paths else "")
    setattr(section_model, field_name, final_val)


def _remove_file(section_model: BaseModel, field_name: str, path_to_delete: str, is_list_type: bool) -> None:
    """Remove an attached file from the model and session state, then refresh."""
    current = getattr(section_model, field_name) or []
    paths = list(current) if isinstance(current, list) else [current]
    
    if path_to_delete in paths:
        paths.remove(path_to_delete)
    if path_to_delete in st.session_state.get("pending_assets", {}):
        del st.session_state.pending_assets[path_to_delete]

    final_val = paths if is_list_type else (paths[0] if paths else "")
    setattr(section_model, field_name, final_val)
    st.rerun()


def _render_file_input(
    section_model: BaseModel, field_name: str, field_info: FieldInfo, label: str, unique_key: str
) -> Any:
    """Render file uploader and handle file attachment/removal UI."""
    is_list_type = _is_list_type(field_info.annotation)
    uploader_key = f"{unique_key}_uploader"
    
    st.file_uploader(
        label,
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=is_list_type,
        key=uploader_key,
        on_change=_handle_file_upload,
        args=(section_model, field_name, uploader_key, is_list_type),
    )

    # Fetch updated paths after callback
    current_val = getattr(section_model, field_name)
    paths = current_val if isinstance(current_val, list) else ([current_val] if current_val else [])
    paths = [p for p in paths if p]

    if paths:
        st.caption(f"🖼️ Attached Files ({len(paths)}):")
        for idx, path in enumerate(paths):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.info(f"`{path}`")
            with col2:
                if st.button("🗑️ Remove", key=f"del_btn_{unique_key}_{idx}"):
                    _remove_file(section_model, field_name, path, is_list_type)

    return paths if is_list_type else (paths[0] if paths else "")


def _render_short_answer(current_val: Any, is_list_type: bool, label: str, unique_key: str) -> Any:
    """Render a text input. Converts lists to comma-separated strings for UI."""
    display_val = ", ".join(current_val) if isinstance(current_val, list) else str(current_val or "")
    user_input = st.text_input(label, value=display_val, key=unique_key)
    
    if is_list_type:
        return [item.strip() for item in user_input.split(",") if item.strip()]
    return user_input


def _render_long_answer(current_val: Any, label: str, unique_key: str) -> str:
    """Render a multiline text area."""
    return st.text_area(label, value=current_val or "", key=unique_key)


def _render_likert_scale(current_val: Any, meta: dict, label: str, unique_key: str) -> int:
    """Render a slider using min/max values from schema metadata."""
    min_val, max_val = int(meta.get("min", 1)), int(meta.get("max", 5))
    slider_val = int(current_val) if current_val is not None else min_val
    return st.slider(label, min_value=min_val, max_value=max_val, value=slider_val, key=unique_key)


def _render_multiple_choice(current_val: Any, meta: dict, label: str, unique_key: str) -> Optional[str]:
    """Render a dropdown selectbox based on schema metadata choices."""
    choices = meta.get("choices", [])
    options = ["-- Select --"] + choices
    default_index = options.index(current_val) if current_val in choices else 0
    
    selected = st.selectbox(label, options=options, index=default_index, key=unique_key)
    return None if selected == "-- Select --" else selected


def render_pydantic_section(section_model: BaseModel, section_key: str) -> Dict[str, Any]:
    """
    Dynamically maps a Pydantic model's fields to Streamlit UI widgets.
    
    Args:
        section_model: The Pydantic model instance with current values.
        section_key: A unique prefix ensuring Streamlit widget keys don't collide.
        
    Returns:
        dict: The updated field values collected from the Streamlit UI.
    """
    updated_values = {}

    for field_name, field_info in type(section_model).model_fields.items():
        current_val = getattr(section_model, field_name)
        label = field_info.description or field_name
        
        meta = field_info.json_schema_extra or {}
        widget = meta.get("widget")
        unique_key = f"{section_key}_{field_name}"

        # Dispatch rendering based on widget type
        if widget in ("FileInput", AnswerType.FILE_INPUT):
            updated_values[field_name] = _render_file_input(
                section_model, field_name, field_info, label, unique_key
            )
            
        elif widget == AnswerType.SHORT_ANSWER:
            is_list = _is_list_type(field_info.annotation)
            updated_values[field_name] = _render_short_answer(current_val, is_list, label, unique_key)
            
        elif widget == AnswerType.LONG_ANSWER:
            updated_values[field_name] = _render_long_answer(current_val, label, unique_key)
            
        elif widget == AnswerType.LIKERT_SCALE:
            updated_values[field_name] = _render_likert_scale(current_val, meta, label, unique_key)
            
        elif widget == AnswerType.MULTIPLE_CHOICE:
            updated_values[field_name] = _render_multiple_choice(current_val, meta, label, unique_key)

    return updated_values