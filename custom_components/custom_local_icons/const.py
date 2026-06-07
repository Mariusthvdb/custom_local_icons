"""Constants for Custom Local Icons integration."""

DOMAIN = "custom_local_icons"
NAME = "Custom Local Icons"
VERSION = "1.2.0"
DESCRIPTION = "Custom local icons, drop in your own svg icons in a folder of choice, and use them in Home Assistant"
URL = "https://github.com/Mariusthvdb/custom_local_icons"

# Frontend JS entrypoint injected into Home Assistant
LOADER_URL = f"/{DOMAIN}/main.js"
LOADER_PATH = f"custom_components/{DOMAIN}/main.js"

# Static SVG hosting endpoint
ICONS_URL = f"/{DOMAIN}/icons"

# Icon picker requests this endpoint for available icon names
ICONLIST_URL = f"/{DOMAIN}/list"

# Info endpoint
INFO_URL = f"/{DOMAIN}/info"
