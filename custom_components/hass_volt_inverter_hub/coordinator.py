#!/usr/bin/env python
"""Volt Inverter Hub – coordinator (v6)

• każdy pojedynczy rejestr Modbus czytany osobno (z przerwą _SLEEP)
• obsługa signed/unsigned, length = 1 lub 2
• per-register „interval” (domyślnie 10 s)
• czujniki złożone (`composite`) są liczone po zaktualizowaniu źródeł
"""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import timedelta
from typing import Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

_SLEEP = 0.03              # 30 ms ciszy pomiędzy ramkami
DEFAULT_INTERVAL = 10      # gdy meta["interval"] nie podano


class VoltCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Centralny punkt odpytywania inwertera Volt przez Modbus."""

    def __init__(self, hass, client, slave: int, registers: dict[str, dict]):
        self.client = client
        self.slave = slave
        self.registers = registers
        self._last_read = {k: 0.0 for k in registers}

        super().__init__(
            hass,
            _LOGGER,
            name="volt_inverter_hub",
            # Tykamy co sekundę; i tak odpytywanie regulują per-rejestr interval-e
            update_interval=timedelta(seconds=1),
        )

    # ------------------------------------------------------------------
    async def _read_single(self, key: str, meta: dict) -> float:
        """Odczytaj jeden rejestr zgodnie z metadanymi i zwróć przeskalowaną wartość."""
        length = meta.get("length", 1)
        addr = meta["addr"]
        fn = meta.get("input_type", "holding")

        if fn == "input":
            rr = await self.client.read_input_registers(addr, length, slave=self.slave)
        else:
            rr = await self.client.read_holding_registers(addr, length, slave=self.slave)

        if rr.isError():
            raise UpdateFailed(rr)

        raw = rr.registers if length > 1 else rr.registers[0]
        if length == 2:                                   # 32-bit (hi << 16 | lo)
            raw = (raw[0] << 16) | raw[1]

        # domyślnie traktujemy jako signed ⇒ można nadpisać {"signed": False}
        if meta.get("signed", True):
            bitlen = 16 * length
            sign_bit = 1 << (bitlen - 1)
            mask = (1 << bitlen) - 1
            if raw & sign_bit:
                raw = -((~raw + 1) & mask)

        return raw * meta["scale"]

    # ------------------------------------------------------------------
    async def _async_update_data(self) -> dict[str, Any]:
        """Aktualizuj wszystkie rejestry zgodnie z ich indywidualnymi interwałami."""
        now = time.monotonic()
        # zaczynamy od poprzednich danych, żeby NIE gubić stanu unavailable → value
        data: dict[str, Any] = {} if self.data is None else dict(self.data)

        for key, meta in self.registers.items():
            # ------- 1. czujniki złożone / aliasy – nie mają addr -------
            if "addr" not in meta:
                if "composite" in meta:
                    total = 0.0
                    ready = True
                    for src in meta["composite"]["sources"]:
                        src_key = src["key"]
                        factor = src.get("factor", 1.0)
                        val = data.get(src_key)
                        if val is None:
                            ready = False
                            break
                        total += val * factor
                    if ready:
                        prec = meta.get("precision")
                        data[key] = round(total, prec) if prec is not None else total
                # jeśli to zwykły alias bez composite – zostawiamy starą wartość
                continue

            # ------- 2. zwykłe rejestry Modbus --------------------------
            interval = meta.get("interval", DEFAULT_INTERVAL)
            if now - self._last_read[key] < interval:
                continue

            try:
                data[key] = await self._read_single(key, meta)
                self._last_read[key] = now
            except Exception as exc:                      # noqa: BLE001
                _LOGGER.debug("Read %s failed: %s", key, exc)
                data[key] = None            # oznacz jako unavailable

            await asyncio.sleep(_SLEEP)

        return data