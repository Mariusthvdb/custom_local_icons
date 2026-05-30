from __future__ import annotations

from homeassistant import config_entries
import voluptuous as vol

DOMAIN = "custom_local_icons"


class CustomLocalIconsConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle config flow for Custom Local Icons."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Initial setup."""

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return await self._show_form(user_input)

    async def async_step_reconfigure(self, user_input=None):
        """Reconfigure existing entry."""

        return await self._show_form(user_input)

    async def _show_form(self, user_input):
        """Shared form logic."""

        errors = {}

        if user_input is not None:
            folder = user_input.get("icon_folder", "").strip()

            if not folder:
                errors["icon_folder"] = "required"
            else:
                return self.async_create_entry(
                    title="Custom Local Icons",
                    data={
                        "icon_folder": folder,
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(
                    "icon_folder",
                    default="www/custom_local_icons",
                ): str,
            }
        )

        return self.async_show_form(
            step_id="user"
            if self.source == config_entries.SOURCE_USER
            else "reconfigure",
            data_schema=schema,
            errors=errors,
        )

# import logging
#
# from homeassistant import config_entries
#
# _LOGGER = logging.getLogger(__name__)
#
#
# @config_entries.HANDLERS.register("custom_local_icons")
# class FontawesomeConfigFlow(config_entries.ConfigFlow):
#     async def async_step_user(self, user_input=None):
#         if self._async_current_entries():
#             return self.async_abort(reason="single_instance_allowed")
#         return self.async_create_entry(title="", data={})
