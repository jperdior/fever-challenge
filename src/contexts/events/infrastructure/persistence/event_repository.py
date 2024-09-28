"""Event Repository Implementation."""

import uuid
import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from src.contexts.events.domain.event import Event
from src.contexts.events.domain.value_objects import EventBaseIdVo, EventTitleVo
from src.contexts.events.infrastructure.persistence.event_model import EventModel
from src.contexts.events.domain.event_repository import EventRepository
from src.shared.domain.vo import DateRangeVo


class EventRepositoryImpl(EventRepository):
    """Event Repository Implementation"""

    def __init__(self, db: SQLAlchemy) -> None:
        super().__init__()
        self.db = db

    def find_by_base_id(self, base_id: int) -> Event|None:
        """Find events by base id."""
        event_model = self.db.session.query(EventModel).filter_by(base_id=base_id).first()
        if not event_model:
            return None
        return self._map_to_domain(event_model)

    def find_by_range(self, start_date: datetime, end_date: datetime) -> list[Event]:
        """Find events by date range."""
        event_models = (
            self.db.session.query(EventModel)
            .filter(
                EventModel.start_date >= start_date,
                EventModel.end_date <= end_date,
                EventModel.sell_mode.is_(True),
            )
            .all()
        )
        return [self._map_to_domain(event_model) for event_model in event_models]

    def save(self, event: Event) -> None:
        """Save an event."""
        logging.info("Saving event %s with id %s", event.title.value, event.aggregate_id)
        event_model = self._map_to_model(event=event)
        self.db.session.merge(event_model)
        self.db.session.commit()

    def _map_to_domain(self, event_model: EventModel) -> Event:
        """Map infra to domain"""
        aggregate_id = str(event_model.id)
        event_base_id = EventBaseIdVo(event_model.base_id)
        title = EventTitleVo(event_model.title)
        date_range = DateRangeVo(
            start_datetime=event_model.start_datetime_to_str(),
            end_datetime=event_model.end_datetime_to_str()
        )
        return Event(
            base_id=event_base_id,
            title=title,
            date_range=date_range,
            min_price=event_model.min_price,
            max_price=event_model.max_price,
            sell_mode=event_model.sell_mode,
            aggregate_id=aggregate_id,
        )
    
    def _map_to_model(self, event: Event) -> EventModel:
        """Map domain to infra"""
        return EventModel(
            id=uuid.UUID(event.aggregate_id),
            base_id=event.base_id.value,
            title=event.title.value,
            start_date=event.date_range.start_datetime,
            end_date=event.date_range.end_datetime,
            min_price=event.min_price,
            max_price=event.max_price,
            sell_mode=event.sell_mode,
        )
