"""Query and query handler for search events use case"""

from typing import List
from dataclasses import dataclass

from src.contexts.events.application.search.service import SearchService
from src.contexts.events.domain.event import Event
from src.contexts.events.domain.exception import DomainError
from src.shared.domain.bus.query import Query, Handler


class SearchEventsQueryType:
    """Query type"""

    SEARCH_EVENTS = "search_events"


@dataclass
class SearchEventsQuery(Query):
    """Search events query"""

    start_datetime: str
    end_datetime: str

    @classmethod
    def type(
        self,
    ) -> str:
        """Query type"""
        return SearchEventsQueryType.SEARCH_EVENTS


class SearchEventsQueryHandler(Handler):
    """Search events query handler"""

    def __init__(self, service: SearchService):
        self.service = service

    def handle(self, query: Query) -> List[Event]:
        """Handle search events query"""
        if not isinstance(query, SearchEventsQuery):
            raise DomainError("Unexpected query", "events.search_events.error", 500)
        events = self.service.execute(
            starts_at=query.start_datetime, ends_at=query.end_datetime
        )
        if not events:
            raise DomainError("Events not found", "events.search_events.error", 404)

        return events
