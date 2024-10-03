"""Tests for the FetchEventsService class."""
from unittest.mock import MagicMock
import pytest
from src.contexts.events.application.parse_and_create.command import ParseAndCreateCommand
from src.contexts.events.domain.provider import EventProvider
from src.shared.domain.bus.command import CommandBus
from src.contexts.events.application.fetch.service import FetchEventsService


@pytest.fixture
def provider():
    return MagicMock(spec=EventProvider)


@pytest.fixture
def command_bus():
    return MagicMock(spec=CommandBus)


@pytest.fixture
def service(provider, command_bus):
    return FetchEventsService(provider=provider, command_bus=command_bus)

def test_service_fetches_events_and_dispatches_commands(service, provider, command_bus):
    """Test that the service fetches events and dispatches commands."""
    event_data_1 = "data from event 1"
    event_data_2 = "data from event 2"
    provider.fetch_events.return_value = [event_data_1, event_data_2]

    service.execute()

    provider.fetch_events.assert_called_once()
    command_bus.dispatch.assert_any_call(ParseAndCreateCommand(event_data=event_data_1))
    command_bus.dispatch.assert_any_call(ParseAndCreateCommand(event_data=event_data_2))
    assert command_bus.dispatch.call_count == 2
