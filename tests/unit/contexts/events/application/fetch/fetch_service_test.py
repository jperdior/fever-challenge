"""Tests for the FetchEventsService class."""

from unittest.mock import MagicMock
import pytest
from src.contexts.events.domain.provider import EventProvider
from src.contexts.events.domain.event_repository import EventRepository
from src.contexts.events.application.fetch.service import FetchEventsService
from src.contexts.events.domain.event import Event


@pytest.fixture
def provider():
    return MagicMock(spec=EventProvider)


@pytest.fixture
def repository():
    return MagicMock(spec=EventRepository)


@pytest.fixture
def service(provider, repository):
    return FetchEventsService(provider=provider, repository=repository)


def test_execute_creates_new_event(service, provider, repository):
    """Should create a new event when it does not exist."""
    event = Event(
        base_id=1,
        title="New Event",
        start_datetime="2023-10-01T10:00:00Z",
        end_datetime="2023-10-01T12:00:00Z",
        min_price=10.0,
        max_price=20.0,
        sell_mode=True,
        aggregate_id="1",
    )
    provider.fetch_events.return_value = [event]
    repository.find_by_base_id.return_value = None

    service.execute()

    repository.save.assert_called_once_with(event=event)


def test_execute_updates_existing_event(service, provider, repository):
    """Should update an existing event."""
    event = Event(
        base_id=1,
        title="Updated Event",
        start_datetime="2023-10-01T10:00:00Z",
        end_datetime="2023-10-01T12:00:00Z",
        min_price=10.0,
        max_price=20.0,
        sell_mode=True,
        aggregate_id="1",
    )
    existing_event = MagicMock(spec=Event)
    existing_event.id = "1"
    provider.fetch_events.return_value = [event]
    repository.find_by_base_id.return_value = existing_event

    service.execute()

    existing_event.update.assert_called_once_with(
        title=event.title,
        start_datetime=event.start_datetime,
        end_datetime=event.end_datetime,
        min_price=event.min_price,
        max_price=event.max_price,
        sell_mode=event.sell_mode,
    )
    repository.save.assert_called_once_with(event=existing_event)


def test_execute_no_events_fetched(service, provider, repository):
    """Should not save any events when none are fetched."""
    provider.fetch_events.return_value = []

    service.execute()

    repository.save.assert_not_called()


def test_execute_multiple_events(service, provider, repository):
    """Should save multiple events."""
    event1 = Event(
        base_id=1,
        title="Event 1",
        start_datetime="2023-10-01T10:00:00Z",
        end_datetime="2023-10-01T12:00:00Z",
        min_price=10.0,
        max_price=20.0,
        sell_mode=True,
        aggregate_id="1",
    )
    event2 = Event(
        base_id=2,
        title="Event 2",
        start_datetime="2023-10-02T10:00:00Z",
        end_datetime="2023-10-02T12:00:00Z",
        min_price=15.0,
        max_price=25.0,
        sell_mode=True,
        aggregate_id="2",
    )
    provider.fetch_events.return_value = [event1, event2]
    repository.find_by_base_id.side_effect = [None, None]

    service.execute()

    repository.save.assert_any_call(event=event1)
    repository.save.assert_any_call(event=event2)
    assert repository.save.call_count == 2
