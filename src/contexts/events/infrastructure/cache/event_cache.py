"""Event Cache Module"""

import json
import hashlib
from typing import List
from src.contexts.events.domain.cache import CacheRepository
from datetime import datetime
from redis import Redis
from src.contexts.events.domain.event import Event


class EventCache(CacheRepository):
    """Event Cache"""

    def __init__(self, cache: Redis):
        self.cache = cache

    def get(self, key: str) -> List[Event]:
        """Get a value from the cache."""
        data = self.cache.get(key)
        if not data:
            return []
        return self._deserialize_events(data)


    def setex(self, key: str, value: List [Event], ttl: int) -> None:
        """Set a value in the cache with a TTL."""
        data = self._serialize_events(value)
        self.cache.setex(key, ttl, data)


    def generate_cache_key(self, start_date: datetime, end_date: datetime) -> str:
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
