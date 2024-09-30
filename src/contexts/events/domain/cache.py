from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from src.contexts.events.domain.event import Event


class CacheRepository(ABC):
    """Abstract class for cache repositories."""

    @abstractmethod
    def get(self, key: str) -> List[Event]:
        """Get a value from the cache."""

    @abstractmethod
    def setex(self, key: str, value: List[Event], ttl: int) -> None:
        """Set a value in the cache with a TTL."""

    @abstractmethod
    def generate_cache_key(self, start_date: datetime, end_date: datetime) -> str:
        """Generates a cache key"""