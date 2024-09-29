"""Event Cache Module"""
from src.contexts.events.domain.cache import CacheRepository
from redis import Redis
from src.contexts.events.domain.event import Event


class EventCache(CacheRepository):
    """Event Cache"""
    def __init__(self, cache: Redis):
        self.cache = cache

    def get(self, key: str)-> str:
        """Get a value from the cache."""
        return self.cache.get(key)

    def set(self, key: str, value: str)->None:
        """Set a value in the cache."""
        self.cache.set(key, value)

    def setex(self, key: str, value: str, ttl: int)->None:
        """Set a value in the cache with a TTL."""
        self.cache.setex(key, ttl, value)