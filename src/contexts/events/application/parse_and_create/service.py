"""Service to fetch events"""

import logging
from src.contexts.events.domain.provider import EventParser
from src.contexts.events.domain.event_repository import EventRepository
from src.contexts.events.domain.event import Event


class ParseAndCreateService:
    """Parse and create Event Service"""

    def __init__(self, repository: EventRepository, parser: EventParser):
        self.repository = repository
        self.parser = parser

    def execute(self, event_data: str) -> None:
        """Execute use case"""
        event: Event = self.parser.parse(data=event_data)
        exists = self.repository.find_by_base_id(base_id=event.base_id)
        if not exists:
            logging.info(
                "Event %s with base ID %d does not exist. Creating it.",
                event.title,
                event.base_id,
            )
            self.repository.save(event=event)
        else:
            logging.info(
                "Event %s with base ID %d and uuid %s exists. Updating it.",
                event.title,
                event.base_id,
                exists.id,
            )
            exists.update(
                title=event.title,
                start_datetime=event.start_datetime,
                end_datetime=event.end_datetime,
                min_price=event.min_price,
                max_price=event.max_price,
                sell_mode=event.sell_mode,
            )
            self.repository.save(event=exists)
