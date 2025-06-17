#!/usr/bin/env python

"""Koordynator z obsługą różnych interwałów per-rejestr."""
from __future__ import annotations
import logging, time
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

class VoltCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, client, slave: int, registers: dict[str, dict]):
        # 1) zapamiętujemy rejestry + czasy ostatniego odczytu
        self.client     = client
        self.slave      = slave
        self.registers  = registers
        now = time.monotonic()
        self._last_read = {k: 0.0 for k in registers}   # 0 ⇒ wymuś pierwszy odczyt

        # 2) wyliczamy NAJKRÓTSZY interwał, żeby wiedzieć jak często “tykać”
        min_interval = min(
            reg.get("interval", 10)           # 10 = UPDATE_INTERVAL
            for reg in registers.values()
        )

        super().__init__(
            hass,
            _LOGGER,
            name="volt_inverter_hub",
            update_interval=timedelta(seconds=min_interval),
        )

    # ------------------------------------------------------------------
    async def _async_update_data(self):
        """Czytamy tylko te rejestry, którym minął ich indywidualny czas."""
        data = {}                        # nowe lub podtrzymane wartości
        now  = time.monotonic()

        for key, meta in self.registers.items():
            interval = meta.get("interval", 10)   # 10 = UPDATE_INTERVAL
            # Czy trzeba już odpytać?
            if now - self._last_read[key] >= interval:
                length = meta.get("length", 1)
                rr = await self.client.read_input_registers(
                    meta["addr"], length, unit=self.slave
                )
                if rr.isError():
                    raise UpdateFailed(rr)

                raw = rr.registers if length > 1 else rr.registers[0]
                if length == 2:               # 32-bit
                    raw = (raw[0] << 16) | raw[1]

                data[key] = raw * meta["scale"]
                self._last_read[key] = now    # znacznik czasu ostatniego sukcesu
            else:
                # Nie odświeżamy – zwracamy poprzednią wartość już znaną
                data[key] = self.data.get(key)

        return data