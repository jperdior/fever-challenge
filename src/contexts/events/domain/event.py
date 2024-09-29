"""
This module represents the Event Aggregate Root.
"""

import uuid
from src.contexts.events.domain.value_objects import EventBaseIdVo, EventTitleVo
from src.shared.domain.aggregate import AggregateRoot
from src.shared.domain.vo import DateRangeVo


class Event(AggregateRoot):
    """
    This class represents the Event Aggregate Root.
    """

    def __init__(
        self,
        base_id: EventBaseIdVo,
        title: EventTitleVo,
        date_range: DateRangeVo,
        min_price: float,
        max_price: float,
        sell_mode: bool,
        aggregate_id: str|None
    ):
        super().__init__(aggregate_id or str(uuid.uuid4()))
        self.base_id = base_id
        self.title = title
        self.date_range = date_range
        self.min_price = min_price
        self.max_price = max_price
        self.sell_mode = sell_mode

    def update(self, title: EventTitleVo, date_range: DateRangeVo, min_price: float, max_price: float, sell_mode: bool):
        """Updates the event."""
        self.title = title
        self.date_range = date_range
        self.min_price = min_price
        self.max_price = max_price
        self.sell_mode = sell_mode

    def to_dict(self) -> dict:
        """Converts the object to a dictionary."""
        return {
            "id": self.id,
            "base_id": self.base_id.value,
            "title": self.title.value,
            "start_date": self.date_range.start_date,
            "start_time": self.date_range.start_time,
            "end_date": self.date_range.end_date,
            "end_time": self.date_range.end_time,
            "min_price": self.min_price,
            "max_price": self.max_price,
            "sell_mode": self.sell_mode
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        """Creates an Event instance from a dictionary."""
        return cls(
            aggregate_id=data["id"],
            base_id=EventBaseIdVo(data["base_id"]),
            title=EventTitleVo(data["title"]),
            date_range=DateRangeVo(
                data["start_date"]+data["start_time"],
                  data["end_date"]+data["end_time"]
                  ),
            min_price=data["min_price"],
            max_price=data["max_price"],
            sell_mode=data["sell_mode"]
        )
