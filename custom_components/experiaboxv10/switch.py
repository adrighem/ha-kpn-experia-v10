"""Switch platform for ExperiaBox v10."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import Device, ExperiaBoxV10Api
from .const import DOMAIN
from .coordinator import ExperiaBoxV10Coordinator, ExperiaBoxV10Data
from .entity import ExperiaBoxV10Entity


@dataclass(kw_only=True, frozen=True)
class ExperiaBoxV10SwitchEntityDescription(SwitchEntityDescription):
    """Class describing ExperiaBox v10 switch entities."""

    is_on_fn: Callable[[ExperiaBoxV10Data], bool | None]
    turn_on_fn: Callable[[ExperiaBoxV10Api], Coroutine[Any, Any, None]]
    turn_off_fn: Callable[[ExperiaBoxV10Api], Coroutine[Any, Any, None]]


SWITCH_TYPES: tuple[ExperiaBoxV10SwitchEntityDescription, ...] = (
    ExperiaBoxV10SwitchEntityDescription(
        key="guest_wifi",
        name="Guest Wi-Fi",
        icon="mdi:wifi-lock",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda data: data.guest_wifi_enabled,
        turn_on_fn=lambda api: api.set_guest_wifi(True),
        turn_off_fn=lambda api: api.set_guest_wifi(False),
    ),
    ExperiaBoxV10SwitchEntityDescription(
        key="global_wifi",
        name="Global Wi-Fi",
        icon="mdi:wifi",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda data: data.wifi_enabled,
        turn_on_fn=lambda api: api.set_wifi(True),
        turn_off_fn=lambda api: api.set_wifi(False),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ExperiaBox v10 switch."""
    coordinator: ExperiaBoxV10Coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        ExperiaBoxV10Switch(coordinator, description) for description in SWITCH_TYPES
    )

    tracked_switches: set[str] = set()

    @callback
    def async_update_entities() -> None:
        """Add new device switches when devices are discovered."""
        if not coordinator.track_devices:
            return
        new_entities = []
        for device in coordinator.data.devices:
            if device.mac not in tracked_switches:
                new_entities.append(
                    ExperiaBoxV10DeviceInternetAccessSwitch(coordinator, device.mac)
                )
                tracked_switches.add(device.mac)

        if new_entities:
            async_add_entities(new_entities)

    async_update_entities()
    entry.async_on_unload(coordinator.async_add_listener(async_update_entities))


class ExperiaBoxV10Switch(ExperiaBoxV10Entity, SwitchEntity):
    """Represent an ExperiaBox v10 switch."""

    entity_description: ExperiaBoxV10SwitchEntityDescription

    def __init__(
        self,
        coordinator: ExperiaBoxV10Coordinator,
        description: ExperiaBoxV10SwitchEntityDescription,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = (
            f"{self.router_unique_id}_{description.key}"
        )

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        return self.entity_description.is_on_fn(self.coordinator.data)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.entity_description.turn_on_fn(self.coordinator.api)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.entity_description.turn_off_fn(self.coordinator.api)
        await self.coordinator.async_request_refresh()


class ExperiaBoxV10DeviceInternetAccessSwitch(ExperiaBoxV10Entity, SwitchEntity):
    """Represent an ExperiaBox v10 per-device internet access switch."""

    _attr_icon = "mdi:web"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: ExperiaBoxV10Coordinator, mac: str) -> None:
        """Initialize the device internet access switch."""
        super().__init__(coordinator)
        self._mac = mac
        self._attr_unique_id = f"{self.router_unique_id}_{mac}_internet_access"

    @property
    def _device(self) -> Device | None:
        """Helper to get device from coordinator."""
        for device in self.coordinator.data.devices:
            if device.mac == self._mac:
                return device
        return None

    @property
    def name(self) -> str:
        """Return the name of the switch."""
        device = self._device
        device_name = device.name if device and device.name else self._mac
        return f"{device_name} Internet Access"

    @property
    def is_on(self) -> bool:
        """Return true if internet access is allowed (not blocked)."""
        sched = self.coordinator.data.parental_schedules.get(self._mac.upper())
        if sched is not None:
            return not sched.blocked
        return True

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        sched = self.coordinator.data.parental_schedules.get(self._mac.upper())
        if sched is not None:
            return {
                "mac": self._mac,
                "scheduled": sched.scheduled,
                "override": sched.override,
                "value": sched.value,
                "rules": sched.rules,
            }
        return {"mac": self._mac, "scheduled": False}

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Enable internet access."""
        await self.coordinator.api.set_parental_control(self._mac, block=False)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Block internet access."""
        await self.coordinator.api.set_parental_control(self._mac, block=True)
        await self.coordinator.async_request_refresh()

