"""Fabryka encji na podstawie metadanych rejestrów."""
from __future__ import annotations
import logging
from typing import Any
from homeassistant.helpers.entity import EntityCategory
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.components.number import NumberEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.select import SelectEntity
from homeassistant.const import Platform
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

def _build_entity(coordinator, key: str):
    meta = coordinator.registers[key]
    if meta.get("is_write_reg"):
        if meta.get("type") == "switch" or meta.get("write_values"):
            return VoltSwitch(coordinator, key)
        if meta.get("options"):
            return VoltSelect(coordinator, key)
        return VoltNumber(coordinator, key)
    return VoltSensor(coordinator, key)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([_build_entity(coordinator, k) for k in coordinator.registers])

# ------------------------------------------------------------------
#  Bazy
# ------------------------------------------------------------------
class VoltBase:
    """Mixin z cechami wspólnymi."""
    def __init__(self, coordinator, key: str):
        self.coordinator = coordinator
        self._key = key
        meta = coordinator.registers[key]
        self._meta = meta
        self._attr_unique_id = f"{DOMAIN}_{key}_{coordinator.slave}"
        self._attr_name      = meta["display_name"]
        if meta.get("is_write_reg"):
            self._attr_entity_category = EntityCategory.CONFIG

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

# ------------------------------------------------------------------
#  Sensor (tylko odczyt)
# ------------------------------------------------------------------
class VoltSensor(VoltBase, SensorEntity):
    def __init__(self, coord, key):
        super().__init__(coord, key)
        self._attr_native_unit_of_measurement = self._meta["unit"]
        dc = self._meta.get("device_class")
        self._attr_device_class = SensorDeviceClass(dc) if dc else None

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)

# ------------------------------------------------------------------
#  Number (czytelny + zapis) 
# ------------------------------------------------------------------
class VoltNumber(VoltBase, NumberEntity):
    def __init__(self, coord, key):
        super().__init__(coord, key)
        self._attr_native_unit_of_measurement = self._meta["unit"]
        self._attr_min_value = self._meta["min"]
        self._attr_max_value = self._meta["max"]
        self._attr_step      = self._meta.get("step", 1)

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)

    async def async_set_native_value(self, value: float):
        await self.coordinator.client.write_register(
            self._meta["addr"],
            round(value / self._meta["scale"]),
            unit=self.coordinator.slave
        )
        await self.coordinator.async_request_refresh()

# ------------------------------------------------------------------
#  Switch
# ------------------------------------------------------------------
class VoltSwitch(VoltBase, SwitchEntity):
    def is_on(self):
        return self.coordinator.data.get(self._key, 0) == 1

    async def async_turn_on(self, **kwargs):
        await self._write(1)

    async def async_turn_off(self, **kwargs):
        await self._write(0)

    async def _write(self, val: int):
        await self.coordinator.client.write_register(
            self._meta["addr"], val, unit=self.coordinator.slave
        )
        await self.coordinator.async_request_refresh()

# ------------------------------------------------------------------
#  Select (lista opcji)
# ------------------------------------------------------------------
class VoltSelect(VoltBase, SelectEntity):
    def __init__(self, coord, key):
        super().__init__(coord, key)
        self._options              = self._meta["options"]
        self._attr_options         = list(self._options.values())

    @property
    def current_option(self):
        raw = self.coordinator.data.get(self._key)
        return self._options.get(raw)

    async def async_select_option(self, option: str):
        for raw, label in self._options.items():
            if label == option:
                await self.coordinator.client.write_register(
                    self._meta["addr"], raw, unit=self.coordinator.slave
                )
                await self.coordinator.async_request_refresh()
                return