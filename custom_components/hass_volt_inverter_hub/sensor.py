"""Platform: sensor – wszystkie rejestry tylko-do-odczytu."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entities import VoltSensor


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        VoltSensor(coordinator, key)
        for key, meta in coordinator.registers.items()
        # brak zapisu, a jednocześnie „expose” nie jest False
        if not meta.get("is_write_reg") and meta.get("expose", True)
    ]
    add_entities(entities, update_before_add=False)