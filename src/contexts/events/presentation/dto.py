"""DTOs for events"""

from typing import List, Union
from dataclasses import dataclass
from src.contexts.events.domain.event import Event
from src.shared.presentation.dto import Error, ResponseDto


@dataclass
class SearchResponseDto(ResponseDto):
    """Search Response DTO"""

    data: Union[List[Event], None]
    error: Union[Error, None]

    def to_dict(self) -> dict:
        """Converts the object to a dictionary."""
        return {
            "data": (
            [
                {k: v for k, v in event.to_dict().items() if k != "sell_mode"}
                for event in self.data
            ]
            if self.data is not None
            else None
            ),
            "error": self.error.to_dict() if self.error is not None else None,
        }
