"""Data Transfer Object"""

from dataclasses import dataclass


@dataclass
class ResponseDto:
    """Response Data Transfer Object, if there were more endpoints
    in the challenge I would have created a PaginatedResponseDto"""

    data: list
    error: str | None = None
