"""Test the ExperiaBox v10 switch platform."""
from unittest.mock import MagicMock, AsyncMock, patch
import pytest

from custom_components.experiaboxv10.coordinator import (
    ExperiaBoxV10Coordinator,
    ExperiaBoxV10Data,
)
from custom_components.experiaboxv10.switch import (
    ExperiaBoxV10Switch,
    ExperiaBoxV10DeviceInternetAccessSwitch,
    SWITCH_TYPES,
    async_setup_entry,
)
from custom_components.experiaboxv10.api import Device, ParentalSchedule, RouterInfo

@pytest.fixture
def hass():
    mock_hass = MagicMock()
    mock_hass.data = {}
    return mock_hass

@pytest.fixture
def entry():
    mock_entry = MagicMock()
    mock_entry.entry_id = "test_entry"
    mock_entry.data = {"host": "1.2.3.4", "username": "u", "password": "p"}
    mock_entry.options = {}
    return mock_entry

@pytest.fixture
def coordinator(hass, entry):
    with patch("custom_components.experiaboxv10.coordinator.async_get_clientsession"):
        coord = ExperiaBoxV10Coordinator(hass, entry)
        hass.data["experiaboxv10"] = {entry.entry_id: coord}
        return coord

@pytest.mark.asyncio
async def test_switch_toggle(coordinator):
    """Test switch toggle actions."""
    mock_router_info = RouterInfo("H369A", "V1.0", "V10.C.26.04", "SN1", 3600)
    coordinator.data = ExperiaBoxV10Data([], mock_router_info, None, None, True)

    switch = ExperiaBoxV10Switch(coordinator, SWITCH_TYPES[0])

    assert switch.is_on is True

    coordinator.api.set_guest_wifi = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()

    await switch.async_turn_off()
    coordinator.api.set_guest_wifi.assert_called_once_with(False)
    coordinator.async_request_refresh.assert_called_once()

    coordinator.api.set_guest_wifi.reset_mock()
    await switch.async_turn_on()
    coordinator.api.set_guest_wifi.assert_called_once_with(True)

@pytest.mark.asyncio
async def test_device_internet_access_switch(coordinator):
    """Test device internet access switch."""
    mac = "AA:BB:CC:DD:EE:01"
    mock_router_info = RouterInfo("H369A", "V1.0", "V10.C.26.04", "SN1", 3600)
    devices = [Device(mac, "Vincent Phone", "192.168.2.10", True)]
    schedules = {
        mac: ParentalSchedule(
            scheduled=True,
            blocked=False,
            rules=[{"day": "Mon"}],
            override=None,
            value="Enable",
        )
    }
    coordinator.data = ExperiaBoxV10Data(
        devices,
        mock_router_info,
        None,
        None,
        True,
        True,
        False,
        None,
        0.0,
        0.0,
        schedules,
    )

    switch = ExperiaBoxV10DeviceInternetAccessSwitch(coordinator, mac)

    assert switch.name == "Vincent Phone Internet Access"
    assert switch.unique_id == f"SN1_{mac}_internet_access"
    assert switch.is_on is True
    assert switch.extra_state_attributes["scheduled"] is True
    assert switch.extra_state_attributes["rules"] == [{"day": "Mon"}]

    coordinator.api.set_parental_control = AsyncMock()
    coordinator.async_request_refresh = AsyncMock()

    await switch.async_turn_off()
    coordinator.api.set_parental_control.assert_called_once_with(mac, block=True)
    coordinator.async_request_refresh.assert_called_once()

    coordinator.api.set_parental_control.reset_mock()
    await switch.async_turn_on()
    coordinator.api.set_parental_control.assert_called_once_with(mac, block=False)

@pytest.mark.asyncio
async def test_async_setup_entry_switches(hass, entry, coordinator):
    """Test async_setup_entry sets up router and device switches."""
    mock_router_info = RouterInfo("H369A", "V1.0", "V10.C.26.04", "SN1", 3600)
    devices = [Device("AA:BB:CC:DD:EE:01", "Phone", "192.168.2.10", True)]
    coordinator.data = ExperiaBoxV10Data(
        devices,
        mock_router_info,
        None,
        None,
        True,
        True,
        False,
        None,
        0.0,
        0.0,
        {},
    )

    added_entities = []

    def mock_add_entities(entities):
        added_entities.extend(entities)

    await async_setup_entry(hass, entry, mock_add_entities)

    # 2 router switches + 1 device switch
    assert len(added_entities) == 3

@pytest.mark.asyncio
async def test_async_setup_entry_switches_disabled_tracking(hass, entry, coordinator):
    """Test async_setup_entry does not add device switches when device tracking is disabled."""
    mock_router_info = RouterInfo("H369A", "V1.0", "V10.C.26.04", "SN1", 3600)
    devices = [Device("AA:BB:CC:DD:EE:01", "Phone", "192.168.2.10", True)]
    coordinator.track_devices = False
    coordinator.data = ExperiaBoxV10Data(
        devices,
        mock_router_info,
        None,
        None,
        True,
        True,
        False,
        None,
        0.0,
        0.0,
        {},
    )

    added_entities = []

    def mock_add_entities(entities):
        added_entities.extend(entities)

    await async_setup_entry(hass, entry, mock_add_entities)

    # Only 2 router switches, no device switches
    assert len(added_entities) == 2

