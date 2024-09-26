"""Search controller module."""

from flask import Request, Response
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
        events: list[Event] = self.search_service.execute()
        return SearchResponseDto(data=events)
