#!/usr/bin/env python
"""Entrypoint integracji Volt Inverter Hub."""
from __future__ import annotations

import asyncio
import logging
import inspect
import voluptuous as vol
from async_timeout import timeout
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
    """Set up Volt Inverter Hub from a config entry."""
    model_key: str = entry.data["model"]
    model_cfg = MODEL_CONFIGS[model_key]

    # 1️⃣  Serial client
    client = AsyncModbusSerialClient(
        port=entry.data["port"],
        baudrate=entry.data["baudrate"],
        parity="N",
        stopbits=1,
        bytesize=8,
        timeout=1,
    )
    await client.connect()

    # 2️⃣  Coordinator
    coordinator = VoltCoordinator(
        hass,
        client=client,
        slave=entry.data.get("slave", model_cfg["default_slave"]),
        registers=model_cfg["registers"],
    )

    # 3️⃣  First refresh – daj 30 s na odpowiedź
    try:
        async with timeout(30):
            await coordinator.async_config_entry_first_refresh()
    except (asyncio.TimeoutError, Exception) as exc:
        _LOGGER.warning("Volt inverter not ready (%s) – will retry later", exc)
        _safe_close(client)
        raise ConfigEntryNotReady from exc

    # 4️⃣  Store & forward platforms
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # 5️⃣  Emergency write_register service
    async def async_write_register(call):
        addr = call.data["address"]
        value = call.data["value"]
        await client.write_register(addr, value, slave=coordinator.slave)

    hass.services.async_register(
        DOMAIN,
        "write_register",
        async_write_register,
        schema=vol.Schema(
            {
                vol.Required("address"): vol.Coerce(int),
                vol.Required("value"): vol.Coerce(int),
            }
        ),
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload integration and close serial link."""
    coordinator: VoltCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
    _safe_close(coordinator.client)
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


def _safe_close(client: AsyncModbusSerialClient) -> None:
    """Close pymodbus client sync or async, depending on version."""
    try:
        if inspect.iscoroutinefunction(client.close):
            # pymodbus ≤ 3.4 had async close()
            coro = client.close()
            asyncio.create_task(coro)
        else:
            client.close()
    except Exception as exc:  # noqa: BLE001
        _LOGGER.debug("Error closing Modbus client: %s", exc)