"""Data Transfer Object"""

from dataclasses import dataclass


@dataclass
class Error:
    """Error Data Transfer Object"""

    message: str
    code: int

    def to_dict(self) -> dict:
        """Converts the object to a dictionary."""
        return {"message": self.message, "code": self.code}


@dataclass
class ResponseDto:
    """Response Data Transfer Object, if there were more endpoints
    in the challenge I would have created a PaginatedResponseDto"""

    data: list | None
    error: Error | None = None
