"""
This module represents the Event Aggregate Root.
"""
from src.shared.domain.aggregate import AggregateRoot

class Event(AggregateRoot):
    """
    This class represents the Event Aggregate Root.
    """
    def __init__(
        self,
        id: str,
        title: str,
        start_date: str,
        start_time: str,
        end_date: str,
        end_time: str,
        min_price: float,
        max_price: float,
    ):
        super().__init__(aggregate_id=id)
        self.title = title
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
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
        