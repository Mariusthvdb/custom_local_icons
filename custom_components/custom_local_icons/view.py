"""HTTP views for Custom Local Icons."""

from __future__ import annotations

import logging
from os import path, walk

from homeassistant.components.http.view import HomeAssistantView

from .const import DOMAIN, NAME, VERSION, DESCRIPTION, URL

_LOGGER = logging.getLogger(__name__)


def scan_icons(base_path: str) -> list[dict]:
    """Scan filesystem recursively and return normalized icon names."""

    icons: list[dict] = []

    for dirpath, _, filenames in walk(base_path):
        rel = path.relpath(dirpath, base_path)
        if rel == ".":
            rel = ""

        for fn in filenames:
            name, ext = path.splitext(fn)

            if ext.lower() != ".svg":
                continue

            full_name = path.join(rel, name) if rel else name
            icons.append({"name": full_name})

    return icons


class ListingView(HomeAssistantView):
    """Serve list of available SVG icons."""

    url = "/custom_local_icons/list"
    name = "Custom Local Icons Listing"
    requires_auth = False

    async def get(self, request):
        """Return icon list."""

        hass = request.app["hass"]
        domain_data = hass.data.get(DOMAIN, {})

        all_icons = []

        for _, data in domain_data.items():
            base_path = data.get("path")

            if not base_path:
                continue

            icons = await hass.async_add_executor_job(
                scan_icons,
                base_path,
            )

            all_icons.extend(icons)

        return self.json(all_icons)


class InfoView(HomeAssistantView):
    """Serve integration metadata."""

    url = "/custom_local_icons/info"
    name = "Custom Local Icons Info"
    requires_auth = False

    async def get(self, request):
        """Return integration info."""

        hass = request.app["hass"]
        domain_data = hass.data.get(DOMAIN, {})

        entry = next(iter(domain_data.values()), {})

        base_path = entry.get("path")
        icon_folder = entry.get("icon_folder")

        def get_svg_count():
            if not base_path:
                return 0
            return len(scan_icons(base_path))

        svg_count = await hass.async_add_executor_job(get_svg_count)

        return self.json(
            {
                "domain": DOMAIN,
                "name": NAME,
                "version": VERSION,
                "description": DESCRIPTION,
                "url": URL,
                "icon_folder": icon_folder,
                "path": base_path,
                "svg_count": svg_count,
            }
        )