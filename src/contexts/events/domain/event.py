"""
This module represents the Event Aggregate Root.
"""

import uuid
from datetime import datetime
from src.contexts.events.domain.value_objects import EventBaseIdVo, EventTitleVo
from src.shared.domain.aggregate import AggregateRoot
from src.shared.domain.vo import DateRangeVo


class Event(AggregateRoot):
    """
    This class represents the Event Aggregate Root.
    """

    def __init__(
        self,
        base_id: int,
        title: str,
        start_datetime: datetime,
        end_datetime: datetime,
        min_price: float,
        max_price: float,
        sell_mode: bool,
        aggregate_id: str | None,
    ):
        super().__init__(aggregate_id or str(uuid.uuid4()))
        self.base_id = base_id
        self.title = title
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.min_price = min_price
        self.max_price = max_price
        self.sell_mode = sell_mode

    @staticmethod
    def create(
        base_id: EventBaseIdVo,
        title: EventTitleVo,
        date_range: DateRangeVo,
        min_price: float,
        max_price: float,
        sell_mode: bool,
    ) -> "Event":
        """Creates a new Event."""
        return Event(
            base_id=base_id.value,
            title=title.value,
            start_datetime=date_range.start_datetime,
            end_datetime=date_range.end_datetime,
            min_price=min_price,
            max_price=max_price,
            sell_mode=sell_mode,
            aggregate_id=None,
        )

    def update(
        self,
        title: str,
        start_datetime: datetime,
        end_datetime: datetime,
        min_price: float,
        max_price: float,
        sell_mode: bool,
    ) -> None:
        """Updates the event."""
        self.title = title
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.min_price = min_price
        self.max_price = max_price
        self.sell_mode = sell_mode

    def to_dict(self) -> dict:
        """Converts the object to a dictionary."""
        return {
            "id": self.id,
            "base_id": self.base_id,
            "title": self.title,
            "start_datetime": self.start_date + " " + self.start_time,
            "end_datetime": self.end_date + " " + self.end_time,
            "min_price": self.min_price,
            "max_price": self.max_price,
            "sell_mode": self.sell_mode,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Event":
        """Creates an Event instance from a dictionary."""
        return cls(
            aggregate_id=data["id"],
            base_id=data["base_id"],
            title=data["title"],
            start_datetime=datetime.strptime(
                data["start_datetime"], "%Y-%m-%d %H:%M:%S"
            ),
            end_datetime=datetime.strptime(data["end_datetime"], "%Y-%m-%d %H:%M:%S"),
            min_price=data["min_price"],
            max_price=data["max_price"],
            sell_mode=data["sell_mode"],
        )

    @property
    def start_date(self) -> str:
        """Returns the start date as a string."""
        return self.start_datetime.strftime("%Y-%m-%d")

    @property
    def start_time(self) -> str:
        """Returns the start time as a string."""
        return self.start_datetime.strftime("%H:%M:%S")

    @property
    def end_date(self) -> str:
        """Returns the end date as a string."""
        return self.end_datetime.strftime("%Y-%m-%d")

    @property
    def end_time(self) -> str:
        """Returns the end time as a string."""
        return self.end_datetime.strftime("%H:%M:%S")
