"""Config flow for Custom Local Icons."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.selector import (
    BooleanSelector,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .const import (
    CONF_ICON_FOLDER,
    DEFAULT_FRONTEND_DEBUG,
    DEFAULT_ICON_FOLDER,
    DOMAIN,
    NAME,
    OPTION_FRONTEND_DEBUG,
)

from .helpers import normalize_folder, validate_folder

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
            folder = normalize_folder(user_input.get(CONF_ICON_FOLDER))
            error = validate_folder(self.hass, folder)

            if error:
                errors[CONF_ICON_FOLDER] = error
            else:
                return self.async_create_entry(
                    title=NAME,
                    data={CONF_ICON_FOLDER: folder},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_ICON_FOLDER,
                        default=DEFAULT_ICON_FOLDER,
                    ): TextSelector(
                        TextSelectorConfig(
                            type=TextSelectorType.TEXT,
                        )
                    ),
                }
            ),
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        """Return options flow."""
        return CustomLocalIconsOptionsFlow()


class CustomLocalIconsOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow."""

    async def async_step_init(self, user_input=None):
        """Manage options."""

        current_folder = self.config_entry.options.get(
            CONF_ICON_FOLDER,
            self.config_entry.data.get(
                CONF_ICON_FOLDER,
                DEFAULT_ICON_FOLDER,
            ),
        )

        current_debug = self.config_entry.options.get(
            OPTION_FRONTEND_DEBUG,
            DEFAULT_FRONTEND_DEBUG,
        )

        errors = {}

        if user_input is not None:
            folder = normalize_folder(user_input.get(CONF_ICON_FOLDER))
            new_debug = user_input.get(
                OPTION_FRONTEND_DEBUG,
                DEFAULT_FRONTEND_DEBUG,
            )

            error = validate_folder(self.hass, folder)

            if error:
                errors[CONF_ICON_FOLDER] = error
            else:
                return self.async_create_entry(
                    title="",
                    data={
                        CONF_ICON_FOLDER: folder,
                        OPTION_FRONTEND_DEBUG: new_debug,
                    },
                )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_ICON_FOLDER,
                        default=current_folder,
                    ): TextSelector(
                        TextSelectorConfig(
                            type=TextSelectorType.TEXT,
                        )
                    ),
                    vol.Optional(
                        OPTION_FRONTEND_DEBUG,
                        default=current_debug,
                    ): BooleanSelector(),
                }
            ),
            errors=errors,
        )