#!/usr/bin/env python
"""Config flow – Volt Inverter Hub (Modbus).

Krok 1
──────
• model   – select (SUPPORTED_MODELS)
• port    – lista wykrytych /dev/serial/by-id/* + <wpisz ręcznie…>
• baudrate, slave

Krok 2 (gdy wybrano „wpisz ręcznie…”)
────────────────────────────────────
• pole tekstowe z portem

Plik wymaga tylko PySerial (już jest w Core HA).
"""

from __future__ import annotations

import os, glob, pathlib
import serial.tools.list_ports
import voluptuous as vol
from typing import Any

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, SUPPORTED_MODELS, DEFAULT_PORT, DEFAULT_BAUDRATE

PORT_MANUAL = "__manual__"          # wewnętrzny identyfikator


# ────────────────────── HELPERS ────────────────────────────────────────
def _friendly_path(device: str) -> str:
    """Zwraca /dev/serial/by-id/… jeśli jest symlinkiem do `device`."""
    for link in glob.glob("/dev/serial/by-id/*"):
        try:
            if os.path.realpath(link) == device:
                return link
        except OSError:
            continue
    return device


def _list_serial_ports() -> list[tuple[str, str]]:
    """Lista (value, label) do formularza."""
    entries = []
    for port in serial.tools.list_ports.comports():
        pretty = _friendly_path(port.device)
        label = f"{pretty}  —  {port.description}"
        entries.append((pretty, label))
    # sortuj po ścieżce
    return sorted(entries, key=lambda x: x[0])


# ────────────────────── CONFIG FLOW ────────────────────────────────────
class VoltConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    # ────────── STEP 1 ────────────────────────────────────────────────
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        ports = _list_serial_ports()
        ports.append((PORT_MANUAL, "<wpisz ręcznie…>"))

        schema = vol.Schema(
            {
                vol.Required("model", default=next(iter(SUPPORTED_MODELS))):
                    vol.In(SUPPORTED_MODELS),
                vol.Required("port", default=DEFAULT_PORT):
                    vol.In(dict(ports)),
                vol.Required("baudrate", default=DEFAULT_BAUDRATE): int,
                vol.Required("slave", default=4): int,
            }
        )

        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=schema)

        if user_input["port"] == PORT_MANUAL:
            self._cache = user_input
            return await self.async_step_port_manual()
        return await self._create_entry(user_input)

    # ────────── STEP 2 (manual port) ──────────────────────────────────
    async def async_step_port_manual(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        schema = vol.Schema({vol.Required("port"): str})

        if user_input is None:
            return self.async_show_form(step_id="port_manual", data_schema=schema)

        data = {**self._cache, **user_input}
        return await self._create_entry(data)

    # ────────── ENTRY HELPER ──────────────────────────────────────────
    async def _create_entry(self, data: dict[str, Any]) -> FlowResult:
        await self.async_set_unique_id(
            f"{data['model']}_{data['port']}_{data['slave']}"
        )
        self._abort_if_unique_id_configured()
        title = f"{SUPPORTED_MODELS[data['model']]}  ({data['port']})"
        return self.async_create_entry(title=title, data=data)

    # ────────── OPTIONS FLOW (prosty) ─────────────────────────────────
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Pozwala zmienić tylko globalny update_interval (sekundy)."""

    def __init__(self, entry: config_entries.ConfigEntry) -> None:
        self.entry = entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(
                    "update_interval",
                    default=self.entry.options.get("update_interval", 10),
                ): vol.All(vol.Coerce(int), vol.Range(min=2, max=300)),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)