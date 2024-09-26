"""Event Repository Implementation."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from src.contexts.events.domain.event import Event
from src.contexts.events.infrastructure.persistence.event_model import EventModel
from src.contexts.events.domain.event_repository import EventRepository



class EventRepositoryImpl(EventRepository):
    """Event Repository Implementation"""

    def __init__(self, db: SQLAlchemy) -> None:
        super().__init__()
        self.db = db


    def find_by_range(self, start_date: datetime, end_date: datetime) -> list[Event]:
        """Find events by date range."""
        events = self.db.session.query(EventModel).filter(
            EventModel.start_date >= start_date, EventModel.end_date <= end_date
        ).all()
        return [Event(
            id=event.id,
            title=event.name,
            date_range=(event.start_date, event.end_date),
            min_price=event.min_price,
            max_price=event.max_price
        ) for event in events]
        

    def save(self, event: Event) -> None:
        """Save an event."""
        