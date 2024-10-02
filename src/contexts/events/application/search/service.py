"""Search Service"""

from typing import List
from src.contexts.events.domain.cache import CacheRepository
from src.contexts.events.domain.event import Event
from src.contexts.events.domain.event_repository import EventRepository
from src.shared.domain.vo import DateRangeVo


class SearchService:
    """Search Service"""

    def __init__(self, repository: EventRepository, cache: CacheRepository):
        self.repository = repository
        self.cache = cache

    def execute(self, starts_at: str, ends_at: str) -> List[Event]:
        """Execute use case"""
        date_range = DateRangeVo(start_datetime=starts_at, end_datetime=ends_at)

        cache_key = self.cache.generate_cache_key(
            date_range.start_datetime, date_range.end_datetime
        )
        cached_events = self.cache.get(cache_key)

        if cached_events:
            return cached_events

        events = self.repository.find_by_range(
            start_date=date_range.start_datetime, end_date=date_range.end_datetime
        )
        if events:
            self.cache.setex(cache_key, events, 60)

        return events
