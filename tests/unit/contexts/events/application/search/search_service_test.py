"""Tests for the search service."""

import pytest
from unittest.mock import MagicMock
from datetime import datetime
from src.contexts.events.application.search.service import SearchService
from src.contexts.events.domain.event import Event
from src.contexts.events.domain.event_repository import EventRepository
from src.contexts.events.domain.cache import CacheRepository
from src.contexts.events.domain.value_objects import EventBaseIdVo
from src.shared.domain.vo import DateRangeVo

EVENTS = [
    Event(
        base_id=1,
        title="Event 1",
        start_datetime=datetime(2021, 7, 21, 17, 32, 28),
        end_datetime=datetime(2021, 7, 21, 18, 32, 28),
        min_price=10.0,
        max_price=20.0,
        sell_mode=True,
        aggregate_id="1",
    ),
    Event(
        base_id=2,
        title="Event 2",
        start_datetime=datetime(2021, 7, 21, 17, 32, 28),
        end_datetime=datetime(2021, 7, 21, 18, 32, 28),
        min_price=10.0,
        max_price=20.0,
        sell_mode=True,
        aggregate_id="2",
    ),
]


@pytest.fixture
def mock_repository():
    return MagicMock(spec=EventRepository)


@pytest.fixture
def mock_cache():
    return MagicMock(spec=CacheRepository)


@pytest.fixture
def search_service(mock_repository, mock_cache):
    return SearchService(repository=mock_repository, cache=mock_cache)


def test_execute_with_cache_hit(search_service, mock_cache):
    """Should return events from cache when cache hit."""
    date_range = DateRangeVo(
        start_datetime="2017-07-21T17:32:28Z", end_datetime="2021-07-21T17:32:28Z"
    )
    cached_events = EVENTS
    mock_cache.get.return_value = cached_events

    events = search_service.execute(date_range)

    assert len(events) == 2
    mock_cache.get.assert_called_once()


def test_execute_with_cache_miss(search_service, mock_repository, mock_cache):
    """Should return events from repository when cache miss."""
    date_range = DateRangeVo(
        start_datetime="2017-07-21T17:32:28Z", end_datetime="2021-07-21T17:32:28Z"
    )
    mock_cache.get.return_value = []
    mock_repository.find_by_range.return_value = EVENTS

    events = search_service.execute(date_range)

    assert len(events) == 2
    mock_cache.get.assert_called_once()
    mock_repository.find_by_range.assert_called_once()
    mock_cache.setex.assert_called_once()


def test_execute_with_cache_miss_and_empty_repository(
    search_service, mock_repository, mock_cache
):
    """Should return empty list when cache miss and repository is empty."""
    date_range = DateRangeVo(
        start_datetime="2017-07-21T17:32:28Z", end_datetime="2021-07-21T17:32:28Z"
    )
    mock_cache.get.return_value = []
    mock_repository.find_by_range.return_value = []

    events = search_service.execute(date_range)

    assert len(events) == 0
    mock_cache.get.assert_called_once()
    mock_repository.find_by_range.assert_called_once()
    mock_cache.setex.assert_not_called()
