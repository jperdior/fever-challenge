"""Service to fetch events"""

from src.contexts.events.application.parse_and_create.command import (
    ParseAndCreateCommand,
)
from src.contexts.events.domain.provider import EventProvider
from src.shared.domain.bus.command import CommandBus


class FetchEventsService:
    """Fetch Events Service"""

    def __init__(self, provider: EventProvider, command_bus: CommandBus):
        self.provider = provider
        self.command_bus = command_bus

    def execute(self) -> None:
        """Execute use case"""
        events_data = self.provider.fetch_events()
        for event_data in events_data:
            self.command_bus.dispatch(ParseAndCreateCommand(event_data=event_data))
