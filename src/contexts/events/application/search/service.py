"""Search Service"""

from typing import List
import hashlib
import json
from datetime import datetime
from src.contexts.events.domain.cache import CacheRepository
from src.contexts.events.domain.event import Event
from src.contexts.events.domain.event_repository import EventRepository
from src.shared.domain.vo import DateRangeVo


class SearchService:
    """Search Service"""

    def __init__(self, repository: EventRepository, cache: CacheRepository):
        self.repository = repository
        self.cache = cache

    def execute(self, date_range: DateRangeVo) -> List[Event]:
        """Execute use case"""
        cache_key = self._generate_cache_key(date_range.start_datetime, date_range.end_datetime)
        cached_events = self.cache.get(cache_key)

        if cached_events:
            return self._deserialize_events(cached_events)

        events = self.repository.find_by_range(
            start_date=date_range.start_datetime, end_date=date_range.end_datetime
        )

        serialized_events = self._serialize_events(events)
        self.cache.setex(cache_key, serialized_events, 60)

        return events

    def _generate_cache_key(self, start_date: datetime, end_date: datetime) -> str:
        """Generates a cache key"""
        key_string = f"events:start={start_date.isoformat()}:end={end_date.isoformat()}:sell_mode=true"
        return hashlib.sha256(key_string.encode()).hexdigest()

    def _serialize_events(self, events: List[Event]) -> str:
        """Serializes a list of events"""
        return json.dumps([event.to_dict() for event in events])

    def _deserialize_events(self, serialized_events: bytes) -> List[Event]:
        """Deserializes a list of events"""
        event_dicts = json.loads(serialized_events)
        return [Event.from_dict(event) for event in event_dicts]


