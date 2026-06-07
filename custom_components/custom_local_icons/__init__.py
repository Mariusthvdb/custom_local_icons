"""Custom Local Icons integration for Home Assistant."""

from __future__ import annotations

import logging

from homeassistant.components.frontend import add_extra_js_url, remove_extra_js_url
from homeassistant.components.http import StaticPathConfig

from .const import DOMAIN, ICONS_URL, ICONLIST_URL, INFO_URL, LOADER_PATH, LOADER_URL
from .view import InfoView, ListingView

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry):
    """Set up integration from config entry."""

    hass.data.setdefault(DOMAIN, {})

    # User-configured folder (relative to HA config, without www prefix)
    user_folder = entry.data["user_folder"].lstrip("/")

    # Convert to absolute filesystem path (automatically add www/)
    path = hass.config.path(f"www/{user_folder}")

    hass.data[DOMAIN][entry.entry_id] = {
        "user_folder": user_folder,
        "path": path,
    }

    # Register static routes:
    #
    # /custom_local_icons/main.js
    # /custom_local_icons/icons/*
    #
    static_paths = [
        StaticPathConfig(
            LOADER_URL,
            hass.config.path(LOADER_PATH),
            True,
        ),
        StaticPathConfig(
            ICONS_URL,
            path,
            True,
        ),
    ]

    await hass.http.async_register_static_paths(static_paths)

    # Register HTTP views
    hass.http.register_view(
        ListingView(
            ICONLIST_URL,
            path,
        )
    )

    hass.http.register_view(
        InfoView(
            INFO_URL,
            hass.data[DOMAIN][entry.entry_id],
        )
    )

    # Inject frontend JS into HA UI
    add_extra_js_url(hass, LOADER_URL)

    LOGGER.info(
        "Custom Local Icons loaded from folder: %s",
        path,
    )

    return True


async def async_unload_entry(hass, entry):
    """Unload integration cleanly."""

    # Remove frontend JS injection
    remove_extra_js_url(hass, LOADER_URL)

    # Clean up data
    hass.data[DOMAIN].pop(entry.entry_id, None)

    LOGGER.info("Custom Local Icons unloaded")

    return True
