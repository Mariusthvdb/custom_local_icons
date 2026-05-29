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

# import logging
# import json
# from os import walk, path
#
# from homeassistant.components.frontend import add_extra_js_url
# from homeassistant.components.http.view import HomeAssistantView
# from homeassistant.components.http import StaticPathConfig  # ✅ Correct import
#
# LOGGER = logging.getLogger(__name__)
#
# DOMAIN = "custom_local_icons"
# LOADER_URL = f'/{DOMAIN}/main.js'
# LOADER_PATH = f'custom_components/{DOMAIN}/main.js'
#
# ICONS_URL = f'/{DOMAIN}/icons'
# ICONLIST_URL = f'/{DOMAIN}/list'
# ICONS_PATH = f'custom_components/{DOMAIN}/data'
#
# CUSTOM_ICONS_URL = f'/{DOMAIN}/icons/pro'
# CUSTOM_ICONS_PATH = 'www/custom_icons/'
#
#
# class ListingView(HomeAssistantView):
#     requires_auth = False
#
#     def __init__(self, url, iconpath):
#         self.url = url
#         self.iconpath = iconpath
#         self.name = "Icon Listing"
#
#     async def get(self, request):
#         icons = []
#         for dirpath, _, filenames in walk(self.iconpath):
#             rel = dirpath[len(self.iconpath):].lstrip(path.sep)
#             icons.extend({"name": path.join(rel, fn[:-4])}
#                          for fn in filenames if fn.endswith(".svg"))
#         return self.json(icons)
#
#
# async def async_setup(hass, config):
#     static_paths = [
#         StaticPathConfig(LOADER_URL, hass.config.path(LOADER_PATH), True),
#         StaticPathConfig(CUSTOM_ICONS_URL, hass.config.path(CUSTOM_ICONS_PATH), True),
#     ]
#
#     for iset in ["brands", "regular", "solid"]:
#         url = f"{ICONS_URL}/{iset}"
#         dirpath = hass.config.path(f"{ICONS_PATH}/{iset}")
#         static_paths.append(StaticPathConfig(url, dirpath, True))
#         hass.http.register_view(ListingView(f"{ICONLIST_URL}/{iset}", dirpath))
#
#     # Register all static paths at once (async, non-blocking)
#     await hass.http.async_register_static_paths(static_paths)
#
#     add_extra_js_url(hass, LOADER_URL)
#
#     # Add pro icons listing
#     pro_dir = hass.config.path(CUSTOM_ICONS_PATH)
#     hass.http.register_view(ListingView(f"{ICONLIST_URL}/pro", pro_dir))
#
#     return True
#
#
# async def async_setup_entry(hass, entry):
#     return True
#
#
# async def async_remove_entry(hass, entry):
#     return True

# from __future__ import annotations
#
# import logging
# from os import path, walk
#
# from homeassistant.components.frontend import add_extra_js_url
# from homeassistant.components.http import StaticPathConfig
# from homeassistant.components.http.view import HomeAssistantView
#
# LOGGER = logging.getLogger(__name__)
#
# DOMAIN = "custom_local_icons"
#
# LOADER_URL = f"/{DOMAIN}/main.js"
# LOADER_PATH = f"custom_components/{DOMAIN}/main.js"
#
# ICONS_URL = f"/{DOMAIN}/icons"
# ICONLIST_URL = f"/{DOMAIN}/list"
#
# # Your SVG folder:
# # /config/www/custom_icons/
# ICONS_PATH = "www/custom_icons"
#
#
# class ListingView(HomeAssistantView):
#     """Return a list of available SVG icons."""
#
#     requires_auth = False
#
#     def __init__(self, url: str, iconpath: str) -> None:
#         self.url = url
#         self.iconpath = iconpath
#         self.name = "Custom Local Icons"
#
#     async def get(self, request):
#         icons = []
#
#         for dirpath, _, filenames in walk(self.iconpath):
#             rel = dirpath[len(self.iconpath):].lstrip(path.sep)
#
#             icons.extend(
#                 {"name": path.join(rel, fn[:-4])}
#                 for fn in filenames
#                 if fn.endswith(".svg")
#             )
#
#         return self.json(icons)
#
#
# async def async_setup(hass, config):
#     """Set up the Custom Local Icons component."""
#
#     icons_dir = hass.config.path(ICONS_PATH)
#
#     static_paths = [
#         StaticPathConfig(
#             LOADER_URL,
#             hass.config.path(LOADER_PATH),
#             True,
#         ),
#         StaticPathConfig(
#             ICONS_URL,
#             icons_dir,
#             True,
#         ),
#     ]
#
#     await hass.http.async_register_static_paths(static_paths)
#
#     hass.http.register_view(
#         ListingView(
#             ICONLIST_URL,
#             icons_dir,
#         )
#     )
#
#     add_extra_js_url(hass, LOADER_URL)
#
#     LOGGER.debug("Custom Local Icons initialized")
#
#     return True
#
#
# async def async_setup_entry(hass, entry):
#     """Set up from config entry."""
#     return True
#
#
# async def async_unload_entry(hass, entry):
#     """Unload config entry."""
#     return True