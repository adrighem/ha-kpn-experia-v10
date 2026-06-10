"""Base entity for ExperiaBox v10."""

from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ExperiaBoxV10Coordinator


class ExperiaBoxV10Entity(CoordinatorEntity[ExperiaBoxV10Coordinator]):
    """Base class for ExperiaBox v10 entities."""

    _attr_has_entity_name = True

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this Experia Box v10."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.router_unique_id)},
            name=self.coordinator.data.router_info.model or "KPN Experia Box v10",
            manufacturer="ZTE",
            model=self.coordinator.data.router_info.model,
            sw_version=self.coordinator.data.router_info.software_version,
            hw_version=self.coordinator.data.router_info.hardware_version,
            configuration_url=f"http://{self.coordinator.api._host}",
        )

    def __init__(self, coordinator: ExperiaBoxV10Coordinator) -> None:
        """Initialize the base entity."""
        super().__init__(coordinator)
        self._router_unique_id = coordinator.router_unique_id

    @property
    def router_unique_id(self) -> str:
        """Return this entity's stable router unique ID."""
        return self._router_unique_id
