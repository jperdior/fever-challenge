"""Search controller module."""

from flask import Request, Response
from src.contexts.events.presentation.error import BadRequestError, InternalServerError
from src.shared.domain.vo import DateRangeVo
from src.shared.presentation.controller import ControllerInterface
from src.contexts.events.application.search.service import SearchService
from src.contexts.events.domain.event import Event
from src.contexts.events.presentation.dto import SearchResponseDto
from src.shared.presentation.dto import ResponseDto


class SearchController(ControllerInterface):
    """Search controller"""

    def __init__(self, search_service: SearchService):
        self.search_service = search_service

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
        try:
            date_range = DateRangeVo(start_datetime=starts_at, end_datetime=ends_at)
        except ValueError as e:
            return SearchResponseDto(data=None, error=BadRequestError(message=str(e)))

        try:
            events: list[Event] = self.search_service.execute(date_range=date_range)
        except Exception:
            return SearchResponseDto(data=None, error=InternalServerError())
        return SearchResponseDto(data=events, error=None)
