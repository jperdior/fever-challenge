from abc import ABC, abstractmethod

from src.contexts.events.domain.event import Event


class CacheRepository(ABC):
    """Abstract class for cache repositories."""

    @abstractmethod
    def get(self, key: str) -> str:
        """Get a value from the cache."""

    @abstractmethod
    def set(self, key: str, value: str) -> None:
        """Set a value in the cache."""

    @abstractmethod
    def setex(self, key: str, value: str, ttl: int) -> None:
        """Set a value in the cache with a TTL."""
        