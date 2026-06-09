"""Constants for Custom Local Icons."""

DESCRIPTION = "Load and render local SVG icons in Home Assistant"
DOMAIN = "custom_local_icons"
NAME = "Custom Local Icons"
URL = "https://github.com/Mariusthvdb/custom_local_icons"

VERSION = "1.3.1"

# Frontend loader
LOADER_URL = f"/{DOMAIN}/main.js"
LOADER_PATH = f"custom_components/{DOMAIN}/main.js"

# Static icon serving
ICONS_URL = f"/{DOMAIN}/icons"

# Icon listing endpoint (used by picker)
ICONLIST_URL = f"/{DOMAIN}/list"

# Info endpoint (important for main.js + debugging)
INFO_URL = f"/{DOMAIN}/info"