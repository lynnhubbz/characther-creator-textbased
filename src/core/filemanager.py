# core/exporter.py
import io
import zipfile
from typing import Dict, Optional


def create_character_bundle(
    character_json: str, assets: Optional[Dict[str, bytes]] = None
) -> bytes:
    """Creates a compressed .zip file containing character.json and asset files.

    :param character_json: The JSON string output from Pydantic model_dump_json()
    :param assets: Dictionary mapping ZIP internal paths to file bytes
                   e.g., {"assets/avatar.png": b"..."}
    """
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. Store the primary JSON data
        zf.writestr("character.json", character_json)

        # 2. Store all associated media assets
        if assets:
            for zip_path, file_bytes in assets.items():
                if file_bytes:
                    zf.writestr(zip_path, file_bytes)

    buffer.seek(0)
    return buffer.getvalue()


def generate_directory_preview(
    asset_paths: list[str]
) -> list[str]:
    """Generates a text-based tree view preview of the zip contents."""
    tree = ["character_bundle.zip", "├── character.json"]
    for i, path in enumerate(asset_paths):
        prefix = "└── " if i == len(asset_paths) - 1 else "├── "
        tree.append(f"{prefix}{path}")
    return tree