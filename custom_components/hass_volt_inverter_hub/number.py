"""Platform: number – wszystkie rejestry edytowalne jako liczba."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entities import VoltNumber


ALLOWED_CLASSES = {
    "voltage",
    "current",
    "power",
    "energy",
    "frequency",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        VoltNumber(coordinator, key)
        for key, meta in coordinator.registers.items()
        if (
            meta.get("is_write_reg")
            and meta.get("device_class") in ALLOWED_CLASSES
            and meta.get("expose", True)
        )
    ]
    add_entities(entities, update_before_add=False)