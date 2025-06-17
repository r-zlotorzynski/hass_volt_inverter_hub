#!/usr/bin/env python

"""Config flow – wybór portu, szybkości, modelu inwertera."""
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from .const import (
    DOMAIN,
    DEFAULT_PORT,
    DEFAULT_BAUDRATE,
    UPDATE_INTERVAL,
    MODEL_CONFIGS,
    SUPPORTED_MODELS,
)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Ładny tytuł kafelka = nazwa wybranego modelu
            title = MODEL_CONFIGS[user_input["model"]]["name"]
            return self.async_create_entry(title=title, data=user_input)

        schema = vol.Schema({
            vol.Required("port",     default=DEFAULT_PORT): str,
            vol.Required("baudrate", default=DEFAULT_BAUDRATE): int,
            vol.Required("slave",    default=list(MODEL_CONFIGS.values())[0]["default_slave"]): int,
            vol.Optional("interval", default=UPDATE_INTERVAL): int,
            vol.Required("model",    default=list(SUPPORTED_MODELS)[0]): vol.In(SUPPORTED_MODELS)
        })
        return self.async_show_form(step_id="user", data_schema=schema)