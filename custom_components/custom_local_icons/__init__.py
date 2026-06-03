from __future__ import annotations

# Used to move blocking filesystem work off the HA event loop
import asyncio

import logging
from os import path, walk

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.http.view import HomeAssistantView

DOMAIN = "custom_local_icons"

LOGGER = logging.getLogger(__name__)

# Frontend JS entrypoint injected into Home Assistant
LOADER_URL = f"/{DOMAIN}/main.js"
LOADER_PATH = f"custom_components/{DOMAIN}/main.js"

# Static SVG hosting endpoint
ICONS_URL = f"/{DOMAIN}/icons"

# Icon picker requests this endpoint for available icon names
ICONLIST_URL = f"/{DOMAIN}/list"


class ListingView(HomeAssistantView):
    """HTTP endpoint that returns all available custom icons."""

    # Must be public so Home Assistant frontend can access it
    requires_auth = False

    def __init__(self, url: str, iconpath: str) -> None:
        self.url = url

        # Absolute filesystem path to icon directory
        self.iconpath = iconpath

        self.name = "Custom Local Icons Listing"

        # Cache to avoid repeated filesystem scans per HA lifecycle
        self._cache: list[dict] | None = None

    def _scan_icons(self) -> list[dict]:
        """Scan filesystem and return icon list."""

        icons = []

        for dirpath, _, filenames in walk(self.iconpath):

            # Convert absolute folder path into relative namespace
            rel = dirpath[len(self.iconpath):].lstrip(path.sep)

            for fn in filenames:
                # Split filename into name + extension safely
                name, ext = path.splitext(fn)

                # Only accept SVG files
                if ext.lower() != ".svg":
                    continue

                # Build icon name (preserves folder structure)
                full_name = path.join(rel, name) if rel else name

                icons.append({"name": full_name})

        return icons

    async def get(self, request):
        """
        Return icon list to frontend.

        Important:
        - Filesystem scanning is blocking I/O
        - Must NOT run on HA event loop

        Therefore:
        - Offloaded to worker thread
        - Cached after first execution
        """

#         # Return cached result if available
#         if self._cache is None:
#
#             # Run blocking filesystem scan
#             # in worker thread.
#             self._cache = await asyncio.to_thread(self._scan_icons)
#
#         return self.json(self._cache)

        icons = await asyncio.to_thread(self._scan_icons)

        LOGGER.info(
            "Custom Local Icons: serving %d icons",
            len(icons),
        )

        return self.json(icons)

async def async_setup_entry(hass, entry):
    """Set up integration from config entry."""

    hass.data.setdefault(DOMAIN, {})

    # User-configured folder (relative to HA config)
    icon_folder = entry.data["icon_folder"].lstrip("/")

    # Convert to absolute filesystem path
    icons_dir = hass.config.path(icon_folder)

    hass.data[DOMAIN][entry.entry_id] = {
        "icon_folder": icon_folder,
        "icons_dir": icons_dir,
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
            icons_dir,
            True,
        ),
    ]

    await hass.http.async_register_static_paths(static_paths)

    # Register icon list endpoint:
    #
    # GET /custom_local_icons/list
    #
    hass.http.register_view(
        ListingView(
            ICONLIST_URL,
            icons_dir,
        )
    )

    # Inject frontend JS into HA UI
    add_extra_js_url(hass, LOADER_URL)

    LOGGER.info(
        "Custom Local Icons loaded from folder: %s",
        icons_dir,
    )

    return True


async def async_unload_entry(hass, entry):
    """Unload integration cleanly."""

    hass.data[DOMAIN].pop(entry.entry_id, None)

    return True
