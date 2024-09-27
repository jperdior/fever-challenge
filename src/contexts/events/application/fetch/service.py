"""Service to fetch events"""

from src.contexts.events.domain.provider import EventProvider
from src.contexts.events.domain.event_repository import EventRepository


class FetchEventsService:
    """Fetch Events Service"""

    def __init__(self, provider: EventProvider, repository: EventRepository):
        self.provider = provider
        self.repository = repository

    def execute(self) -> None:
        """Execute use case"""
        events = self.provider.fetch_events()
        for event in events:
            exists = self.repository.find_by_base_id(base_id=event.base_id.value)
            if not exists:
                self.repository.save(event=event)
            else:
                event.update(
                    title=event.title,
                    date_range=event.date_range,
                    min_price=event.min_price,
                    max_price=event.max_price,
                    sell_mode=event.sell_mode,
                )
                self.repository.save(event=event)