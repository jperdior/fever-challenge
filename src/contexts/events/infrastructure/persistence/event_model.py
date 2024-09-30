"""Event model module"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, func
from src.shared.infrastructure.persistence.postgresql import DB


class EventModel(DB.Model):
    """Event model class"""

    __tablename__ = "events"

    base_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    min_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    sell_mode = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at = Column(DateTime, default=None, nullable=True)

    def __repr__(self):
        return (
            f"<EventModel(id={self.id}, title={self.title}, start_date={self.start_date}, "
            f"end_date={self.end_date}, min_price={self.min_price}, "
            f"max_price={self.max_price}, sell_mode={self.sell_mode})>"
        )

    def start_datetime_to_str(self) -> str:
        """Converts start datetime to string"""
        return self.start_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    def end_datetime_to_str(self) -> str:
        """Converts end datetime to string"""
        return self.end_datetime.strftime("%Y-%m-%dT%H:%M:%S")
