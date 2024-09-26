"""Service to fetch events"""

import asyncio
from src.contexts.events.domain.provider import EventProvider


class FetchEventsService:
    """Fetch Events Service"""

    def __init__(self, provider: EventProvider):
        self.provider = provider

    def execute(self) -> None:
        """Execute use case"""
        self.provider.fetch_events()
