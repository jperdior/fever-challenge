"""Event Repository Implementation."""

import uuid
import logging
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

    def find_by_base_id(self, base_id: int) -> Event | None:
        """Find events by base id."""
        event_model = (
            self.db.session.query(EventModel).filter_by(base_id=base_id).first()
        )
        if not event_model:
            return None
        return self._map_to_domain(event_model)

    def find_by_range(self, start_date: datetime, end_date: datetime) -> list[Event]:
        """Find events by date range."""
        event_models = (
            self.db.session.query(EventModel)
            .filter(
                EventModel.start_datetime >= start_date,
                EventModel.end_datetime <= end_date,
                EventModel.sell_mode.is_(True),
            )
            .all()
        )
        return [self._map_to_domain(event_model) for event_model in event_models]

    def save(self, event: Event) -> None:
        """Save an event."""
        logging.info("Saving event %s with id %s", event.title, event.id)
        event_model = self._map_to_model(event=event)
        self.db.session.merge(event_model)
        self.db.session.commit()

    def _map_to_domain(self, event_model: EventModel) -> Event:
        """Map infra to domain"""

        return Event(
            base_id=event_model.base_id,
            title=event_model.title,
            start_datetime=event_model.start_datetime,
            end_datetime=event_model.end_datetime,
            min_price=event_model.min_price,
            max_price=event_model.max_price,
            sell_mode=event_model.sell_mode,
            aggregate_id=str(event_model.id),
        )

    def _map_to_model(self, event: Event) -> EventModel:
        """Map domain to infra"""
        return EventModel(
            id=uuid.UUID(event.id),
            base_id=event.base_id,
            title=event.title,
            start_datetime=event.start_datetime,
            end_datetime=event.end_datetime,
            min_price=event.min_price,
            max_price=event.max_price,
            sell_mode=event.sell_mode,
        )
