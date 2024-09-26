"""This module contains the abstract class for event providers."""

from abc import ABC, abstractmethod

from src.contexts.events.domain.event import Event


class EventProvider(ABC):
    """Abstract class for event providers."""

    @abstractmethod
    def fetch_events(self) -> None:
        """Fetch events from the provider."""

    @abstractmethod
    def parse_events(self, data: str) -> list[Event]:
        """Parse the fetched data into a standard format."""

    @abstractmethod
    def store_events(self, events: list[Event]) -> None:
        """Store the parsed events in the database."""
