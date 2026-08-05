import typing
from typing import Any, Dict, Optional
from uuid import uuid4

import streamlit as st
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from streamlit_sortables import sort_items

from ....core import base


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


def _unwrap_annotation(annotation: Any) -> Any:
    args = typing.get_args(annotation)
    if len(args) == 2 and type(None) in args:
        return next(arg for arg in args if arg is not type(None))
    return annotation


def _coerce_short_answer_value(raw_value: Any, annotation: Any, is_list_type: bool) -> Any:
    if is_list_type:
        return [item.strip() for item in str(raw_value or "").split(",") if item.strip()]

    if raw_value is None:
        return ""

    text_value = str(raw_value)
    if not text_value.strip():
        target_type = _unwrap_annotation(annotation)
        if target_type is int:
            return 0
        if target_type is float:
            return 0.0
        return ""

    target_type = _unwrap_annotation(annotation)
    if target_type is int:
        try:
            return int(text_value)
        except ValueError:
            return 0

    if target_type is float:
        try:
            return float(text_value)
        except ValueError:
            return 0.0

    return text_value


def _render_short_answer(
    current_val: Any, is_list: bool, label: str, unique_key: str, annotation: Any
) -> Any:
    display_val = ", ".join(current_val) if isinstance(current_val, list) else str(current_val or "")
    user_input = st.text_input(label, value=display_val, key=unique_key)
    return _coerce_short_answer_value(user_input, annotation, is_list)


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

def _render_multiple_choice_custom(
    current_val: Any, meta: dict, label: str, unique_key: str
) -> Optional[str]:
    """Render a dropdown selectbox with an 'Other...' option for custom text input."""
    choices = meta.get("choices", [])
    custom_option = "Other..."
    options = ["-- Select --"] + choices + [custom_option]

    # Calculate default index
    default_index = 0
    if current_val in choices:
        default_index = options.index(current_val)
    elif current_val:  # Has a value, but not in standard choices -> custom value
        default_index = options.index(custom_option)

    # 1. Render Dropdown
    selected = st.selectbox(
        label, options=options, index=default_index, key=f"{unique_key}_select"
    )

    if selected == "-- Select --":
        return None

    # 2. Render Custom Input if "Other..." is selected
    if selected == custom_option:
        # Pre-fill text box if current value is a custom string
        default_custom_text = str(current_val) if current_val and current_val not in choices else ""
        
        custom_input = st.text_input(
            f"Specify custom value for {label}:",
            value=default_custom_text,
            key=f"{unique_key}_custom_text",
            placeholder="Type custom entry here...",
        )
        return custom_input.strip() if custom_input.strip() else None

    return selected

def _normalize_multi_short_items(current_val: Any) -> list[dict[str, str]]:
    if not current_val:
        return [{"id": str(uuid4()), "value": ""}]

    normalized: list[dict[str, str]] = []

    for item in current_val:
        if isinstance(item, dict):
            normalized.append({
                "id": str(item.get("id") or uuid4()),
                "value": str(item.get("value", ""))
            })
        else:
            normalized.append({
                "id": str(uuid4()),
                "value": str(item)
            })

    return normalized

def _render_multiple_short_answer(
    current_val: Any,
    label: str,
    unique_key: str
) -> list[str]:

    state_key = f"{unique_key}_items"

    if state_key not in st.session_state:
        st.session_state[state_key] = _normalize_multi_short_items(current_val)

    items = st.session_state[state_key]

    st.caption(label)

    if st.button("＋ Add", key=f"{unique_key}_add"):
        items.append({"id": str(uuid4()), "value": ""})
        st.session_state[state_key] = items
        st.rerun()

    cleaned_items: list[dict[str, str]] = []

    for item in items:
        item_id = item["id"]
        item_value = item["value"]

        col_input, col_delete = st.columns([5, 1])

        with col_input:
            new_value = st.text_input(
                "",
                value=item_value,
                key=f"{unique_key}_{item_id}",
                label_visibility="collapsed",
            )
            cleaned_items.append({"id": item_id, "value": new_value})

        with col_delete:
            if st.button("🗑", key=f"{unique_key}_del_{item_id}"):
                items = [row for row in items if row["id"] != item_id]
                st.session_state[state_key] = items
                st.rerun()

    st.session_state[state_key] = cleaned_items
    
    return [row["value"].strip() for row in cleaned_items if row["value"].strip()]

def render_pydantic_section(
    section_model: BaseModel, 
    section_key: str, 
    skip_nested: bool = True  # <-- Add flag here (defaults to False)
    ) -> dict:
    updated_values = {}

    for field_name, field_info in type(section_model).model_fields.items():
        current_val = getattr(section_model, field_name)
        label = field_info.description or field_name
        unique_key = f"{section_key}_{field_name}"

        # =================================================================
        # 1. NESTED MODEL CHECK
        # =================================================================
        if isinstance(current_val, BaseModel):
            if skip_nested:
                continue  # <-- Skips nested models like General_Body!

            st.markdown(f"#### ↳ {label}")
            with st.container(border=True):
                nested_updates = render_pydantic_section(
                    current_val, unique_key, skip_nested=skip_nested
                )
                for k, v in nested_updates.items():
                    setattr(current_val, k, v)
                updated_values[field_name] = current_val
            
            continue

        # =================================================================
        # 2. STANDARD WIDGETS (For flat fields like strings, ints, etc.)
        # =================================================================
        meta = field_info.json_schema_extra or {}
        widget = meta.get("widget") # type:ignore cuz somehow the code worked

        # Dispatch rendering based on widget type
        if widget in ("FileInput", base.AnswerType.FILE_INPUT):
            updated_values[field_name] = _render_file_input(
                section_model, field_name, field_info, label, unique_key
            )
            
        elif widget == base.AnswerType.SHORT_ANSWER:
            is_list = _is_list_type(field_info.annotation)
            updated_values[field_name] = _render_short_answer(
                current_val, is_list, label, unique_key, field_info.annotation
            )
            
        elif widget == base.AnswerType.LONG_ANSWER:
            updated_values[field_name] = _render_long_answer(current_val, label, unique_key)
            
        elif widget == base.AnswerType.LIKERT_SCALE:
            updated_values[field_name] = _render_likert_scale(current_val, meta, label, unique_key) # type:ignore cuz somehow the code worked
            
        elif widget == base.AnswerType.MULTIPLE_CHOICE:
            updated_values[field_name] = _render_multiple_choice(current_val, meta, label, unique_key) # type:ignore cuz somehow the code worked

        elif widget == base.AnswerType.MULTIPLE_CHOICE_CUSTOM:
            updated_values[field_name] = _render_multiple_choice_custom(
                current_val, meta, label, unique_key
            )

        elif widget == base.AnswerType.MULTIPLE_SHORT_ANSWER:
            updated_values[field_name] = _render_multiple_short_answer(
                current_val, label, unique_key
            )
    return updated_values

