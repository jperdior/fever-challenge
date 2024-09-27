"""Presentation Error"""

from src.shared.presentation.dto import Error


class BadRequestError(Error):
    """Bad Request Error"""

    def __init__(self, message: str):
        super().__init__(message, 400)


class InternalServerError(Error):
    """Internal Server Error"""

    def __init__(self):
        super().__init__("Internal Server Error", 500)
