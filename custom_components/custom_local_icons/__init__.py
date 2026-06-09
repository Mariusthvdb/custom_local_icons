"""Custom Local Icons integration."""

from __future__ import annotations

import logging

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig

from .const import (
    DOMAIN,
    LOADER_URL,
    LOADER_PATH,
    ICONS_URL,
)

from .view import ListingView, InfoView

LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Global setup (register HTTP views once)."""

    hass.http.register_view(ListingView())
    hass.http.register_view(InfoView())

    return True


async def async_setup_entry(hass, entry) -> bool:
    """Set up Custom Local Icons from config entry."""

    first_entry = DOMAIN not in hass.data or not hass.data.get(DOMAIN)

    hass.data.setdefault(DOMAIN, {})

    # -----------------------------------------------------
    # Use options first (updated via OptionsFlow), fallback to data
    # -----------------------------------------------------
    icon_folder = (
        entry.options.get(
            "icon_folder",
            entry.data["icon_folder"],
        )
    ).strip().lstrip("/")

    # -----------------------------------------------------
    # ALWAYS resolve inside /config/www
    # -----------------------------------------------------
    path = hass.config.path("www", icon_folder)

    LOGGER.info("=== Custom Local Icons ===")
    LOGGER.info("Icon folder: %s", icon_folder)
    LOGGER.info("Path: %s", path)

    # Store runtime data
    hass.data[DOMAIN][entry.entry_id] = {
        "icon_folder": icon_folder,
        "path": path,
    }

    # -----------------------------------------------------
    # Static paths (NO MANUAL UNREGISTER)
    # -----------------------------------------------------
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

    # Load frontend script only once
    if first_entry:
        add_extra_js_url(hass, LOADER_URL)

    # -----------------------------------------------------
    # Reload listener (OptionsFlow support)
    # -----------------------------------------------------
    entry.async_on_unload(
        entry.add_update_listener(async_update_listener)
    )

    LOGGER.info(
        "Custom Local Icons loaded from folder: %s",
        path,
    )

    return True


async def async_unload_entry(hass, entry) -> bool:
    """Unload integration."""

    hass.data[DOMAIN].pop(entry.entry_id, None)

    if not hass.data[DOMAIN]:
        try:
            from homeassistant.components.frontend import remove_extra_js_url

            remove_extra_js_url(hass, LOADER_URL)
        except Exception:
            pass

        hass.data.pop(DOMAIN, None)

    LOGGER.info("Custom Local Icons unloaded")

    return True


# ---------------------------------------------------------
# OptionsFlow reload hook
# ---------------------------------------------------------
async def async_update_listener(hass, entry):
    """Reload integration when options change."""

    new_folder = entry.options.get(
        "icon_folder",
        entry.data.get("icon_folder"),
    )

    LOGGER.info(
        "Custom Local Icons configuration changed, reloading with folder: %s",
        new_folder,
    )

    await hass.config_entries.async_reload(entry.entry_id)
