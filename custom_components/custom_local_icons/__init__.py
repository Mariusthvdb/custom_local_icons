from __future__ import annotations

import logging
from os import path, walk

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.http.view import HomeAssistantView

DOMAIN = "custom_local_icons"

LOGGER = logging.getLogger(__name__)

LOADER_URL = f"/{DOMAIN}/main.js"
LOADER_PATH = f"custom_components/{DOMAIN}/main.js"

ICONS_URL = f"/{DOMAIN}/icons"
ICONLIST_URL = f"/{DOMAIN}/list"


class ListingView(HomeAssistantView):
    """Return list of SVG icons."""

    requires_auth = False

    def __init__(self, url: str, iconpath: str) -> None:
        self.url = url
        self.iconpath = iconpath
        self.name = "Custom Local Icons Listing"

    async def get(self, request):
        icons = []

        for dirpath, _, filenames in walk(self.iconpath):
            rel = dirpath[len(self.iconpath):].lstrip(path.sep)

            icons.extend(
                {"name": path.join(rel, fn[:-4])}
                for fn in filenames
                if fn.endswith(".svg")
            )

        return self.json(icons)


async def async_setup_entry(hass, entry):
    """Set up from config entry."""

    hass.data.setdefault(DOMAIN, {})

    icon_folder = entry.data["icon_folder"].lstrip("/")
    icons_dir = hass.config.path(icon_folder)

    hass.data[DOMAIN][entry.entry_id] = {
        "icon_folder": icon_folder,
        "icons_dir": icons_dir,
    }

    static_paths = [
        StaticPathConfig(
            LOADER_URL,
            hass.config.path(LOADER_PATH),
            True,
        ),
        StaticPathConfig(
            ICONS_URL,
            icons_dir,
            True,
        ),
    ]

    await hass.http.async_register_static_paths(static_paths)

    hass.http.register_view(
        ListingView(
            ICONLIST_URL,
            icons_dir,
        )
    )

    add_extra_js_url(hass, LOADER_URL)

    LOGGER.debug(
        "Custom Local Icons loaded with folder: %s",
        icons_dir,
    )

    return True


async def async_unload_entry(hass, entry):
    """Unload config entry."""

    hass.data[DOMAIN].pop(entry.entry_id, None)

    return True
