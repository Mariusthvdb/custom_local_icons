"""Config flow for Custom Local Icons."""

from __future__ import annotations

import logging

from homeassistant import config_entries
import voluptuous as vol

DOMAIN = "custom_local_icons"
LOGGER = logging.getLogger(__name__)


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
                # Handle reconfiguration
                if self.source == config_entries.SOURCE_RECONFIGURE:
                    self.hass.config_entries.async_update_entry(
                        self.config_entry,
                        data={
                            "user_folder": folder,
                        },
                    )
                    LOGGER.info(
                        "Custom Local Icons reconfigured with new folder: %s",
                        folder,
                    )
                    await self.hass.config_entries.async_reload(
                        self.config_entry.entry_id
                    )
                    return self.async_abort(reason="reconfigure_successful")

                # Handle initial setup
                return self.async_create_entry(
                    title="Custom Local Icons",
                    data={
                        "user_folder": folder,
                    },
                )

        # Get default folder from existing entry if reconfiguring
        default_folder = "custom_local_icons"
        if self.source == config_entries.SOURCE_RECONFIGURE:
            default_folder = self.config_entry.data.get(
                "user_folder", "custom_local_icons"
            )

        schema = vol.Schema(
            {
                vol.Required(
                    "user_folder",
                    default=default_folder,
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
