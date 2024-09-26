"""DTOs for events"""

from typing import List
from dataclasses import dataclass
from src.contexts.events.domain.event import Event
from src.shared.presentation.dto import ResponseDto


@dataclass
class SearchResponseDto(ResponseDto):
    """Search Response DTO"""

    data: List[Event]
    error: str | None = None

    def to_dict(self) -> dict:
        """Converts the object to a dictionary."""
        return {"data": [event.to_dict() for event in self.data], "error": self.error}
