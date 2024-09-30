"""DTOs for events"""

from typing import List, Union
from dataclasses import dataclass
from src.shared.presentation.dto import Error, ResponseDto


@dataclass
class EventResponseDto:
    """Event Response DTO"""

    id: str
    title: str
    start_date: str
    start_time: str
    end_date: str
    end_time: str
    min_price: float
    max_price: float

    def to_dict(self) -> dict:
        """Converts the object to a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "start_date": self.start_date,
            "start_time": self.start_time,
            "end_date": self.end_date,
            "end_time": self.end_time,
            "min_price": self.min_price,
            "max_price": self.max_price,
        }


@dataclass
class SearchResponseDto(ResponseDto):
    """Search Response DTO"""

    data: Union[List[EventResponseDto], None]
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
