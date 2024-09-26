"""Search Service"""
from typing import List
from src.contexts.events.domain.event import Event

class SearchService:
    """Search Service"""

    def execute(self) -> List[Event]:
        """Execute use case"""
        events: list[Event] = [
            Event(
                id="1",
                title="Event 1",
                start_date="2021-01-01",
                start_time="10:00",
                end_date="2021-01-01",
                end_time="12:00",
                min_price=10.0,
                max_price=20.0,
            ),
            Event(
                id="2",
                title="Event 2",
                start_date="2021-01-01",
                start_time="10:00",
                end_date="2021-01-01",
                end_time="12:00",
                min_price=10.0,
                max_price=20.0,
            ),
            Event(
                id="3",
                title="Event 3",
                start_date="2021-01-01",
                start_time="10:00",
                end_date="2021-01-01",
                end_time="12:00",
                min_price=10.0,
                max_price=20.0,
            ),
        ]

        return events
