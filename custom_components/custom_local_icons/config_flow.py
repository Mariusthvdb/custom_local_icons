"""Config flow for Custom Local Icons."""

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
            folder = user_input.get("user_folder", "").strip()

            if not folder:
                errors["user_folder"] = "required"
            else:
                return self.async_create_entry(
                    title="Custom Local Icons",
                    data={
                        "user_folder": folder,
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(
                    "user_folder",
                    default="custom_local_icons",
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
