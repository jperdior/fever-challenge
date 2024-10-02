"""This module contains the abstract class for event providers."""

from abc import ABC, abstractmethod

from src.contexts.events.domain.event import Event


class EventProvider(ABC):
    """Abstract class for event providers."""

    @abstractmethod
    def fetch_events(self) -> list[str]:
        """Fetch events from the provider."""


class EventParser(ABC):
    """Abstract class for event parsers."""

    @abstractmethod
    def parse(self, data: str) -> Event | None:
        """Parse the fetched data into a standard format."""
