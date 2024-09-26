"""
This module represents the Event Aggregate Root.
"""

from src.contexts.events.domain.value_objects import EventIdVo, EventTitleVo
from src.shared.domain.aggregate import AggregateRoot
from src.shared.domain.vo import DateRangeVo


class Event(AggregateRoot):
    """
    This class represents the Event Aggregate Root.
    """

    def __init__(
        self,
        id: EventIdVo,
        title: EventTitleVo,
        date_range: DateRangeVo,
        min_price: float,
        max_price: float,
    ):
        super().__init__(aggregate_id=id.value)
        self.title = title.value
        self.start_date = date_range.start_date
        self.start_time = date_range.start_time
        self.end_date = date_range.end_date
        self.end_time = date_range.end_time
        self.min_price = min_price
        self.max_price = max_price

    def to_dict(self) -> dict:
        """Converts the object to a dictionary."""
        return {
            "id": self.aggregate_id,
            "title": self.title,
            "start_date": self.start_date,
            "start_time": self.start_time,
            "end_date": self.end_date,
            "end_time": self.end_time,
            "min_price": self.min_price,
            "max_price": self.max_price,
        }
