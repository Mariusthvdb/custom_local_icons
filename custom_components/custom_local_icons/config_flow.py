"""Config flow for Custom Local Icons."""

from __future__ import annotations

import logging
from os import path

import voluptuous as vol

from homeassistant import config_entries

DOMAIN = "custom_local_icons"

LOGGER = logging.getLogger(__name__)


class CustomLocalIconsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for Custom Local Icons."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle initial setup."""

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        errors = {}

        if user_input is not None:
            folder = (user_input.get("icon_folder") or "").strip().lstrip("/")

            error = self._validate_folder(folder)

            if error:
                errors["icon_folder"] = error
            else:
                return self.async_create_entry(
                    title="Custom Local Icons",
                    data={"icon_folder": folder},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=self._schema("custom_local_icons"),
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        """Return options flow."""
        return CustomLocalIconsOptionsFlow()

    def _validate_folder(self, folder: str) -> str | None:
        """Validate folder inside /config/www."""

        if not folder:
            return "required"

        abs_path = self.hass.config.path("www", folder)

        try:
            if not path.isdir(abs_path):
                return "folder_not_found"
        except Exception:
            return "invalid_path"

        return None

    @staticmethod
    def _schema(default: str):
        """Build form schema."""

        return vol.Schema(
            {
                vol.Required(
                    "icon_folder",
                    default=default,
                ): str,
            }
        )


class CustomLocalIconsOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    async def async_step_init(self, user_input=None):
        """Manage options."""

        LOGGER.info(
            "Custom Local Icons options opened. Current options: %s",
            dict(self.config_entry.options),
        )

        errors = {}

        current_folder = self.config_entry.options.get(
            "icon_folder",
            self.config_entry.data.get(
                "icon_folder",
                "custom_local_icons",
            ),
        )

        if user_input is not None:
            folder = (user_input.get("icon_folder") or "").strip().lstrip("/")

            error = self._validate_folder(folder)

            if error:
                errors["icon_folder"] = error
            else:
                LOGGER.info(
                    "Custom Local Icons configuration changed, new folder: %s",
                    folder,
                )

                return self.async_create_entry(
                    title="",
                    data={"icon_folder": folder},
                )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "icon_folder",
                        default=current_folder,
                    ): str,
                }
            ),
            errors=errors,
        )

    def _validate_folder(self, folder: str) -> str | None:
        """Validate folder inside /config/www."""

        if not folder:
            return "required"

        abs_path = self.hass.config.path("www", folder)

        try:
            if not path.isdir(abs_path):
                return "folder_not_found"
        except Exception:
            return "invalid_path"

        return None
