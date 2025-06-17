from __future__ import annotations
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class VoltBase:
    """Mixin z koordynatorem, metadanymi i wspólnym device_info."""

    def __init__(self, coordinator, key: str):
        self.coordinator = coordinator
        self._key = key
        self._meta = coordinator.registers[key]
        self._scale = self._meta.get("scale", 1)

        # unikalny identyfikator i nazwa
        self._attr_unique_id = key
        self._attr_name = self._meta.get("display_name")
        self._attr_device_class = self._meta.get("device_class")

        # przypiszemy encję do jednego z kilku „urządzeń” w device registry
        group = self._meta.get("group") or self._determine_group(key)
        title = self._group_title(group)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{coordinator.entry_id}_{group}")},
            name=f"{coordinator.model_name} – {title}",
            manufacturer="VOLT",
            model=coordinator.model_name,
        )

    def _determine_group(self, key: str) -> str:
        """Określa grupę na podstawie klucza i meta."""
        if self._meta.get("is_write_reg"):
            return "settings"
        if key.startswith("volt_mppt_"):
            return "mppt"
        if key.startswith("volt_battery_"):
            return "battery"
        # grid / sieć
        if "_grid_" in key or key.startswith("volt_power_grid") or key.startswith("volt_q_grid"):
            return "grid"
        # inverter / zasilanie wyspowe
        if key.startswith("volt_inverter_") or key.startswith("volt_power_inverter"):
            return "inverter"
        return "general"

    def _group_title(self, group: str) -> str:
        """Przyjazne nazwy grup."""
        return {
            "settings": "Settings",
            "mppt": "MPPT",
            "battery": "Battery",
            "grid": "Grid",
            "inverter": "Inverter",
            "general": "General",
        }.get(group, group.title())

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
        val = self.coordinator.data.get(self._key)
        if val is None:
            return None
        prec = self._meta.get("precision")
        return round(val, prec) if prec is not None else val


# ------------------------------------------------------------------
class VoltNumber(VoltBase, NumberEntity):
    """Rejestr zapisowy jako encja Number."""

    def __init__(self, coordinator, key: str):
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
        await self.coordinator.client.write_register(
            self._addr, raw, slave=self.coordinator.slave
        )
        await self.coordinator.async_request_refresh()


# ------------------------------------------------------------------
class VoltSwitch(VoltBase, SwitchEntity):
    """Przełącznik ON/OFF (0/1)."""

    def __init__(self, coordinator, key: str):
        super().__init__(coordinator, key)
        self._addr = self._meta["addr"]

    @property
    def is_on(self):
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._key) == 1

    async def async_turn_on(self, **kwargs):
        await self.coordinator.client.write_register(
            self._addr, 1, slave=self.coordinator.slave
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.client.write_register(
            self._addr, 0, slave=self.coordinator.slave
        )
        await self.coordinator.async_request_refresh()


# ------------------------------------------------------------------
class VoltSelect(VoltBase, SelectEntity):
    """Rejestr z listą opcji (encja Select)."""

    def __init__(self, coordinator, key: str):
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
                await self.coordinator.client.write_register(
                    self._addr, raw, slave=self.coordinator.slave
                )
                await self.coordinator.async_request_refresh()
                return
        raise ValueError(f"Option {option} not found for {self._attr_name}")