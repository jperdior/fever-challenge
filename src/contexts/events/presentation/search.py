"""Search controller module."""

from flask import Request
from src.contexts.events.presentation.error import BadRequestError
from src.shared.presentation.controller import ControllerInterface
from src.contexts.events.domain.event import Event
from src.contexts.events.presentation.dto import EventResponseDto, SearchResponseDto
from src.shared.presentation.dto import ResponseDto
from src.contexts.events.application.search.query import SearchEventsQuery
from src.shared.infrastructure.bus.query import QueryBus


class SearchController(ControllerInterface):
    """Search controller"""

    def __init__(self, query_bus: QueryBus):
        self.query_bus = query_bus

    def execute(self, request: Request) -> ResponseDto:
        """Executes the search controller"""
        starts_at = request.args.get("starts_at")
        ends_at = request.args.get("ends_at")
        if not starts_at:
            return SearchResponseDto(
                data=None, error=BadRequestError(message="starts_at is required")
            )
        ends_at = request.args.get("ends_at")
        if not ends_at:
            return SearchResponseDto(
                data=None, error=BadRequestError(message="ends_at is required")
            )

        events: list[Event] = self.query_bus.ask(
            query=SearchEventsQuery(start_datetime=starts_at, end_datetime=ends_at)
        )

        events_dto = [
            EventResponseDto(
                id=event.id,
                title=event.title,
                start_date=event.start_date,
                start_time=event.start_time,
                end_date=event.end_date,
                end_time=event.end_time,
                min_price=event.min_price,
                max_price=event.max_price,
            )
            for event in events
        ]
        return SearchResponseDto(data=events_dto, error=None)
