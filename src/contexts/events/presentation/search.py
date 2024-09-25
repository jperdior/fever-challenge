from src.shared.presentation.controller import ControllerInterface
from flask import Request, Response


class SearchController(ControllerInterface):
    def __init__(self, search_use_case: SearchUseCase):
        self.search_use_case = search_use_case

    def execute(self, request: Request) -> Response:
        try:
            query = request.query
            events = self.search_use_case.execute(query)
            return Response(events)
        except Exception as e:
            return Response(str(e), status=400)