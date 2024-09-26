from abc import ABC, abstractmethod
from datetime import datetime

from src.contexts.events.domain.event import Event


class EventRepository(ABC):
    """Abstract class for event repositories."""

    @abstractmethod
    def find_by_range(self, start_date: datetime, end_date: datetime) -> list[Event]:
        """Find events by date range."""

    @abstractmethod
    def save(self, event: Event) -> None:
        """Save an event."""