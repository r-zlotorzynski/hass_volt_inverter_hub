#!/usr/bin/env python

"""Entrypoint integracji Volt Inverter Hub."""
from __future__ import annotations
import logging, voluptuous as vol
from pymodbus.client import AsyncModbusSerialClient
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from .const import DOMAIN, MODEL_CONFIGS
from .coordinator import VoltCoordinator

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.NUMBER, Platform.SWITCH, Platform.SELECT]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Tworzymy klienta Modbus, koordynator i encje."""
    model_key: str = entry.data["model"]
    model_cfg     = MODEL_CONFIGS[model_key]

    client = AsyncModbusSerialClient(
        method="rtu",
        port=entry.data["port"],
        baudrate=entry.data["baudrate"],
        stopbits=1, bytesize=8, parity="N", timeout=1
    )
    await client.connect()

    coordinator = VoltCoordinator(
        hass,
        client=client,
        slave=entry.data.get("slave", model_cfg["default_slave"]),
        registers=model_cfg["registers"]
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Uniwersalny serwis write_register (awaryjnie, gdy encji brak)
    async def async_write_register(call):
        addr  = call.data["address"]
        value = call.data["value"]
        await client.write_register(addr, value, unit=coordinator.slave)
    hass.services.async_register(
        DOMAIN, "write_register", async_write_register,
        schema=vol.Schema({"address": vol.Coerce(int), "value": vol.Coerce(int)})
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator: VoltCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
    await coordinator.client.close()
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)