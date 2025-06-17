# custom_components/hass_volt_inverter_hub/entities.py

from __future__ import annotations
import logging
import os
import json

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.number import NumberEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class VoltBase:
    """Mixin z koordynatorem, metadanymi i wspólnym DeviceInfo."""

    def __init__(self, coordinator, key: str):
        self.coordinator = coordinator
        self._key = key
        self._meta = coordinator.registers[key]
        self._scale = self._meta.get("scale", 1)

        # ✅ unikalny identyfikator encji
        self._attr_unique_id = key
        # 2) PODPOWIEDŹ dla entity_registry,
        #    dzięki czemu entity_id przyjmie formę sensor.volt_battery_voltage
        self._attr_suggested_object_id = key
        # ✅ użyj wbudowanego mechanizmu tłumaczeń HA
        #    HA automatycznie zaczyta z translations/<lang>.json:
        #    entity.sensor.<key>.name etc.
        self._attr_translation_key = key
        self._attr_has_entity_name = True

        # ✅ device_class, jeśli jest
        self._attr_device_class = self._meta.get("device_class")

        # ——— grupowanie na poziomie DeviceInfo —–
        group = self._meta.get("group", "general")
        title = self._load_group_title(group)

        # self._attr_device_info = DeviceInfo(
        #     identifiers={(DOMAIN, f"{coordinator.entry_id}_{group}")},
        #     name=f"{coordinator.model_name} – {title}",
        #     manufacturer="VOLT",
        #     model=coordinator.model_name,
        # )
         # każde "urządzenie" (grupa) ma własne DeviceInfo
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{coordinator.entry_id}_{group}")},
            # nazwa widoczna w UI = sama nazwa grupy (PL/EN z pliku translations)
            name=title, # wersja bez nazwy modelu
            # name=f"{coordinator.model_name} – {title}", # wersja z nazwą modelu
            manufacturer="Volt",
            # pełna nazwa modelu można zostawić w atrybucie 'model' (niewidoczna w nagłówku)
            model=coordinator.model_name
        )


    def _load_group_title(self, group: str) -> str:
        """Wczytaj tytuł grupy z translations/<lang>.json → sekcja 'group'."""
        lang = self.coordinator.hass.config.language
        path = os.path.join(
            os.path.dirname(__file__),
            "translations",
            f"{lang}.json",
        )
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            return data.get("group", {}).get(group, group.title())
        except Exception as e:
            _LOGGER.debug("Nie udało się wczytać tłumaczeń grupy %s: %s", group, e)
            return group.title()

    @property
    def available(self) -> bool:
        return self.coordinator.data is not None


# ------------------------------------------------------------------
class VoltSensor(VoltBase, SensorEntity):
    """Sensor tylko-do-odczytu."""

    def __init__(self, coordinator, key):
        super().__init__(coordinator, key)
        # ↓ wymuszamy stały identyfikator
        self.entity_id = f"sensor.{key}"

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
    """Rejestr zapisywalny jako encja Number."""

    def __init__(self, coordinator, key):
        super().__init__(coordinator, key)
        self.entity_id = f"number.{key}"
        self._attr_native_unit_of_measurement = self._meta.get("unit")
        self._attr_native_min_value = self._meta.get("min")
        self._attr_native_max_value = self._meta.get("max")
        self._attr_native_step = self._meta.get("step", 1)
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
        self.entity_id = f"switch.{key}"
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
        self.entity_id = f"select.{key}"
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