"""Helpers for Custom Local Icons."""

from os import path
from .const import CONF_ICON_FOLDER


def normalize_folder(folder: str) -> str:
    """Light normalization only (HA-safe)."""

    return (folder or "").strip().lstrip("/")


def validate_folder(hass, folder: str) -> str | None:
    """Validate folder exists in /config/www."""

    if not folder:
        return "required"

    abs_path = hass.config.path("www", folder)

    try:
        if not path.isdir(abs_path):
            return "folder_not_found"
    except OSError:
        return "invalid_path"

    return None


def get_icon_folder(entry) -> str:
    """Return effective icon folder from options or config entry data."""

    return entry.options.get(
        CONF_ICON_FOLDER,
        entry.data.get(CONF_ICON_FOLDER),
    )