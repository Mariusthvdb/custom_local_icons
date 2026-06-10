"""Config flow for Custom Local Icons."""

from __future__ import annotations

import logging
from os import path

import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN, OPTION_FRONTEND_DEBUG, DEFAULT_FRONTEND_DEBUG

LOGGER = logging.getLogger(__name__)


def validate_folder(hass, folder: str) -> str | None:
    """Validate folder inside /config/www."""

    if not folder:
        return "required"

    abs_path = hass.config.path("www", folder)

    try:
        if not path.isdir(abs_path):
            return "folder_not_found"
    except Exception:
        return "invalid_path"

    return None


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

            error = validate_folder(self.hass, folder)

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

        current_folder = self.config_entry.options.get(
            "icon_folder",
            self.config_entry.data.get(
                "icon_folder",
                "custom_local_icons",
            ),
        )

        current_debug = self.config_entry.options.get(
            OPTION_FRONTEND_DEBUG,
            DEFAULT_FRONTEND_DEBUG,
        )

        errors = {}

        if user_input is not None:
            folder = (user_input.get("icon_folder") or "").strip().lstrip("/")
            new_debug = user_input.get(
                OPTION_FRONTEND_DEBUG,
                DEFAULT_FRONTEND_DEBUG,
            )

            error = validate_folder(self.hass, folder)

            if error:
                errors["icon_folder"] = error
            else:
                if folder != current_folder:
                    LOGGER.info(
                        "Custom Local Icons folder changed: %s → %s",
                        current_folder,
                        folder,
                    )

                if new_debug != current_debug:
                    LOGGER.info(
                        "Custom Local Icons debug changed: %s → %s",
                        current_debug,
                        new_debug,
                    )

                return self.async_create_entry(
                    title=None,
                    data={
                        "icon_folder": folder,
                        OPTION_FRONTEND_DEBUG: new_debug,
                    },
                )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "icon_folder",
                        default=current_folder,
                    ): str,
                    vol.Required(
                        OPTION_FRONTEND_DEBUG,
                        default=current_debug,
                    ): bool,
                }
            ),
            errors=errors,
        )
