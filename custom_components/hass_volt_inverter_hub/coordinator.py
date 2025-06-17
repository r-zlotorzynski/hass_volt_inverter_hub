#!/usr/bin/env python
"""Volt Inverter Hub – coordinator v7
   • jedna pętla „na okrągło” czyta rejestry po kolei
   • pauza _SLEEP po każdym udanym odczycie
   • indywidualny „interval” nadal działa
   • self.async_set_updated_data(...) wysyła stan od razu
"""

from __future__ import annotations

import asyncio, logging, time
from typing import Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

_SLEEP = 0.05       # 50 ms ciszy po KAŻDEJ ramce


class VoltCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Ciągłe skanowanie Modbus z odstępem _SLEEP."""

    def __init__(self, hass, client, slave: int, registers: dict[str, dict]):
        super().__init__(hass, _LOGGER, name="volt_inverter_hub")
        self.client, self.slave = client, slave
        self.registers = registers

        self.data: dict[str, Any] = {k: None for k in registers}
        self._last_read = {k: 0.0 for k in registers}

        # osobna task-pętla
        self._task = hass.loop.create_task(self._worker())

    # ------------------------------------------------------------------
    async def _worker(self):
        """Bez końca: idź po rejestrach; szanuj ich ‘interval’."""
        keys = list(self.registers)
        idx = 0

        while True:
            key = keys[idx]
            idx = (idx + 1) % len(keys)
            meta = self.registers[key]

            # composite / brak addr → pomijamy (liczymy osobno niżej)
            if "addr" not in meta:
                await asyncio.sleep(_SLEEP)
                continue

            now = time.monotonic()
            if now - self._last_read[key] < meta.get("interval", 10):
                await asyncio.sleep(0)          # yield
                continue

            # reconnect w razie potrzeby
            if not self.client.connected:
                try:
                    await self.client.connect()
                except Exception:               # noqa: BLE001
                    await asyncio.sleep(1)
                    continue

            try:
                value = await self._read_single(meta)
                self.data[key] = value
                self._last_read[key] = now
            except Exception as exc:            # noqa: BLE001
                _LOGGER.debug("Reg %s fail: %s", key, exc)
                self.data[key] = None

            # przelicz composite przy każdym udanym odczycie
            self._update_composites()
            # powiadom HA (asynchronicznie)
            self.async_set_updated_data(self.data.copy())

            await asyncio.sleep(_SLEEP)

    # ------------------------------------------------------------------
    def _update_composites(self):
        for key, meta in self.registers.items():
            if "composite" not in meta:
                continue
            total = 0.0
            missing = False
            for part in meta["composite"]["sources"]:
                val = self.data.get(part["key"])
                if val is None:
                    missing = True
                    break
                total += val * part["factor"]
            self.data[key] = None if missing else total

    # ------------------------------------------------------------------
    async def _read_single(self, meta: dict) -> float:
        addr, length = meta["addr"], meta.get("length", 1)
        fn = meta.get("input_type", "holding")

        rr = (
            await self.client.read_input_registers(addr, length, slave=self.slave)
            if fn == "input"
            else await self.client.read_holding_registers(addr, length, slave=self.slave)
        )
        if rr.isError():
            raise ValueError(rr)

        raw = rr.registers if length > 1 else rr.registers[0]
        if length == 2:
            raw = (raw[0] << 16) | raw[1]

        if meta.get("signed", True):
            bitlen = 16 * length
            if raw & (1 << (bitlen - 1)):
                raw = raw - (1 << bitlen)

        return raw * meta["scale"]

    # ------------------------------------------------------------------
    async def async_close(self):
        """Nadpisz: zatrzymaj pętlę przy wyłączaniu integracji."""
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        await self.client.close()