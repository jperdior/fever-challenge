"""Search Service"""

from typing import List
from datetime import datetime
from src.contexts.events.domain.event import Event
from src.contexts.events.domain.event_repository import EventRepository
from src.shared.domain.vo import DateRangeVo


class SearchService:
    """Search Service"""

    def __init__(self, repository: EventRepository):
        self.repository = repository

    def execute(self, date_range: DateRangeVo) -> List[Event]:
        """Execute use case"""
        print("Searching events...")
        events = self.repository.find_by_range(
            start_date=date_range.start_datetime, end_date=date_range.end_datetime
        )

        return events
