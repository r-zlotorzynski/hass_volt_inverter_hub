#!/usr/bin/env python
"""Entrypoint integracji Volt Inverter Hub."""
from __future__ import annotations

import async_timeout
import logging
import voluptuous as vol
from pymodbus.client import AsyncModbusSerialClient
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, MODEL_CONFIGS
from .coordinator import VoltCoordinator

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.NUMBER,
    Platform.SWITCH,
    Platform.SELECT,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Utwórz klienta Modbus, koordynatora i zarejestruj encje."""
    cfg = entry.data
    model_cfg = MODEL_CONFIGS[cfg["model"]]

    client = AsyncModbusSerialClient(
        port=cfg["port"],
        baudrate=cfg["baudrate"],
        parity="N",
        stopbits=1,
        bytesize=8,
        timeout=1,
    )

    # szybki test połączenia
    try:
        async with async_timeout.timeout(3):
            await client.connect()
            if not client.connected:               # ←–––– JEDYNA ISTOTNA ZMIANA
                raise ConfigEntryNotReady("Serial port busy / not found")
    except Exception as exc:
        _LOGGER.debug("Modbus connect error: %s", exc)
        client.close()
        raise ConfigEntryNotReady("Serial port init failed") from exc

    coordinator = VoltCoordinator(
        hass,
        client=client,
        slave=cfg.get("slave", model_cfg["default_slave"]),
        registers=model_cfg["registers"],
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # awaryjny serwis „write_register”
    async def async_write_register(call):
        addr = call.data["address"]
        value = call.data["value"]
        await client.write_register(addr, value, slave=coordinator.slave)

    hass.services.async_register(
        DOMAIN,
        "write_register",
        async_write_register,
        schema=vol.Schema({"address": vol.Coerce(int), "value": vol.Coerce(int)}),
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Graceful unload."""
    coordinator: VoltCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
    coordinator.client.close()          # sync – bez await
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)