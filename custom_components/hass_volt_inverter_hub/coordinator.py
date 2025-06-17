#!/usr/bin/env python
"""Volt Inverter Hub – coordinator v8 (blokowy odczyt Modbus).

 • Przy starcie generuje listę bloków (start, length, fn, keys[]).
 • Jeden worker loop idzie po blokach i czyta hurtowo (max 125 reg.).
 • Blok odpytywany tylko, gdy któryś klucz > interval.
 • Pauza _SLEEP po każdej udanej ramce.
 • Obsługa signed=True, precision, composite, auto-reconnect.
"""

from __future__ import annotations

import asyncio, logging, time
from typing import Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)
_SLEEP = 0.05           # 50 ms ciszy pomiędzy ramkami RTU
_MAX_REG = 125          # limit Modbus RTU


class VoltCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Koordynator z hurtowym odczytem bloków."""

    # ------------------------------------------------------------------
    def __init__(self, hass, client, slave: int, registers: dict[str, dict]):
        super().__init__(hass, _LOGGER, name="volt_inverter_hub")
        self.client, self.slave = client, slave
        self.registers = registers

        self.data: dict[str, Any] = {k: None for k in registers}
        self._last_read = {k: 0.0 for k in registers}

        self._blocks = self._make_blocks()
        self._task = hass.loop.create_task(self._worker())

    # ------------------------------------------------------------------
    # ---------- BLOKOWANIE REJESTRÓW -----------------------------------
    def _make_blocks(self):
        """Zwraca listę bloków (start, length, fn, keys[(key, addr)])"""
        regs = sorted(
            (
                (key, meta["addr"], meta.get("input_type", "holding"))
                for key, meta in self.registers.items()
                if "addr" in meta           # pomija composite/expose False
            ),
            key=lambda x: (x[2], x[1])      # sortuj po fn, następnie addr
        )

        blocks = []
        cur_keys, cur_start, cur_fn = [], None, None
        prev_addr = None

        for key, addr, fn in regs:
            new_block = (
                cur_start is None
                or fn != cur_fn
                or addr - prev_addr > 1
                or addr - cur_start >= _MAX_REG
            )
            if new_block and cur_keys:
                blocks.append(
                    (cur_start, prev_addr - cur_start + 1, cur_fn, cur_keys)
                )
                cur_keys, cur_start, cur_fn = [], None, None

            if cur_start is None:
                cur_start, cur_fn = addr, fn
            cur_keys.append((key, addr))
            prev_addr = addr

        if cur_keys:
            blocks.append((cur_start, prev_addr - cur_start + 1, cur_fn, cur_keys))

        _LOGGER.debug("Modbus blocks generated: %s", blocks)
        return blocks

    # ------------------------------------------------------------------
    async def _worker(self):
        """Niekończąca się pętla: skanuje bloki i publikuje dane."""
        while True:
            now = time.monotonic()
            for start, length, fn, keys in self._blocks:
                # czy któryś klucz w bloku już „wygasł”?
                if not any(
                    now - self._last_read[k] >= self.registers[k].get("interval", 10)
                    for k, _ in keys
                ):
                    continue

                if not self.client.connected:
                    try:
                        await self.client.connect()
                    except Exception:        # noqa: BLE001
                        await asyncio.sleep(1)
                        continue

                try:
                    await self._read_block(start, length, fn, keys)
                    self._update_composites()
                    self.async_set_updated_data(self.data.copy())
                except Exception as exc:    # noqa: BLE001
                    _LOGGER.debug("Block %s-%s (%s) fail: %s",
                                  start, start + length - 1, fn, exc)
                await asyncio.sleep(_SLEEP)

    # ------------------------------------------------------------------
    async def _read_block(self, start: int, length: int, fn: str, keys):
        """Czyta blok i rozpakowuje do self.data."""
        rr = (
            await self.client.read_input_registers(start, length, slave=self.slave)
            if fn == "input"
            else await self.client.read_holding_registers(start, length, slave=self.slave)
        )
        if rr.isError():
            raise ValueError(rr)

        for key, addr in keys:
            meta = self.registers[key]
            offset = addr - start
            val = rr.registers[offset]

            # 32-bit?  (length==2 w meta)  –> połącz dwa słowa
            if meta.get("length", 1) == 2:
                upper = rr.registers[offset + 1]
                val = (val << 16) | upper

            # signed?
            if meta.get("signed", True):
                bitlen = 16 * meta.get("length", 1)
                signbit = 1 << (bitlen - 1)
                if val & signbit:
                    val = val - (1 << bitlen)

            scaled = val * meta["scale"]
            self.data[key] = scaled
            self._last_read[key] = time.monotonic()

    # ------------------------------------------------------------------
    def _update_composites(self):
        for key, meta in self.registers.items():
            comp = meta.get("composite")
            if not comp:
                continue
            total = 0.0
            missing = False
            for src in comp["sources"]:
                v = self.data.get(src["key"])
                if v is None:
                    missing = True
                    break
                total += v * src["factor"]
            self.data[key] = None if missing else round(
                total, meta.get("precision", 3)
            )

    # ------------------------------------------------------------------
    async def async_close(self):
        """Zatrzymaj worker przy wyładowaniu integracji."""
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        await self.client.close()