# custom_components/hass_volt_inverter_hub/entities.py
from __future__ import annotations
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.select import SelectEntity

_LOGGER = logging.getLogger(__name__)


class VoltBase:
    """Mixin z koordinatorem, metadanymi i cechami wspólnymi."""

    def __init__(self, coordinator, key):
        self.coordinator = coordinator
        self._key = key
        self._meta = coordinator.registers[key]
        self._scale = self._meta.get("scale", 1)

        self._attr_unique_id = key
        self._attr_name = self._meta.get("display_name")
        self._attr_device_class = self._meta.get("device_class")

    @property
    def available(self) -> bool:
        return self.coordinator.data is not None


# ------------------------------------------------------------------
class VoltSensor(VoltBase, SensorEntity):
    """Sensor tylko-do-odczytu."""

    @property
    def native_unit_of_measurement(self):
        return self._meta.get("unit")

    @property
    def native_value(self):
        if self.coordinator.data is None:
            return None
        value = self.coordinator.data.get(self._key)
        if value is None:
            return None
        prec = self._meta.get("precision")
        return round(value, prec) if prec is not None else value


# ------------------------------------------------------------------
class VoltNumber(VoltBase, NumberEntity):
    """Rejestr do zapisu jako encja Number."""

    def __init__(self, coordinator, key):
        super().__init__(coordinator, key)
        self._attr_native_unit_of_measurement = self._meta.get("unit")
        self._attr_min_value = self._meta.get("min")
        self._attr_max_value = self._meta.get("max")
        self._attr_step = self._meta.get("step", 1)
        self._addr = self._meta["addr"]

    @property
    def native_value(self):
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._key)

    async def async_set_native_value(self, value: float):
        raw = int(round(value / self._scale))
        await self.coordinator.client.write_register(self._addr, raw, slave=self.coordinator.slave)
        await self.coordinator.async_request_refresh()


# ------------------------------------------------------------------
class VoltSwitch(VoltBase, SwitchEntity):
    """Przełącznik ON/OFF na bazie rejestru 0/1."""

    def __init__(self, coordinator, key):
        super().__init__(coordinator, key)
        self._addr = self._meta["addr"]

    @property
    def is_on(self):
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._key) == 1

    async def async_turn_on(self, **kwargs):
        await self.coordinator.client.write_register(self._addr, 1, slave=self.coordinator.slave)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.client.write_register(self._addr, 0, slave=self.coordinator.slave)
        await self.coordinator.async_request_refresh()


# ------------------------------------------------------------------
class VoltSelect(VoltBase, SelectEntity):
    """Rejestr z listą opcji (encja Select)."""

    def __init__(self, coordinator, key):
        super().__init__(coordinator, key)
        self._addr = self._meta["addr"]
        self._options_dict = self._meta["options"]
        self._attr_options = list(self._options_dict.values())

    @property
    def current_option(self):
        if self.coordinator.data is None:
            return None
        raw = self.coordinator.data.get(self._key)
        return self._options_dict.get(raw)

    async def async_select_option(self, option: str):
        for raw, label in self._options_dict.items():
            if label == option:
                await self.coordinator.client.write_register(self._addr, raw, slave=self.coordinator.slave)
                await self.coordinator.async_request_refresh()
                return
        raise ValueError(f"Option {option} not found for {self._attr_name}")