"""
This module represents the Event Aggregate Root.
"""

import uuid
from src.contexts.events.domain.value_objects import EventIdVo, EventTitleVo
from src.shared.domain.aggregate import AggregateRoot
from src.shared.domain.vo import DateRangeVo


class Event(AggregateRoot):
    """
    This class represents the Event Aggregate Root.
    """

    def __init__(
        self,
        base_id: EventIdVo,
        title: EventTitleVo,
        date_range: DateRangeVo,
        min_price: float,
        max_price: float,
        sell_mode: bool,
        aggregate_id: str|None = None,
    ):
        if aggregate_id:
            super().__init__(aggregate_id=aggregate_id)
        else:
            uid = uuid.uuid4()
            super().__init__(aggregate_id=str(uid))
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
            "id": self.aggregate_id,
            "title": self.title,
            "start_date": self.date_range.start_date,
            "start_time": self.date_range.start_time,
            "end_date": self.date_range.end_date,
            "end_time": self.date_range.end_time,
            "min_price": self.min_price,
            "max_price": self.max_price,
        }
