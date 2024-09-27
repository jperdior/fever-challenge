"""Event model module"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, func
from src.shared.infrastructure.persistence.postgresql import DB


class EventModel(DB.Model):
    """Event model class"""

    __tablename__ = "events"

    id = Column(String, primary_key=True)
    base_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    min_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    sell_mode = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at = Column(DateTime, default=None, nullable=True)

    def __init__(
        self,
        aggregate_id: str,
        base_id: int,
        title: str,
        start_date: datetime,
        end_date: datetime,
        min_price: float,
        max_price: float,
        sell_mode: bool,
    ):
        self.id = aggregate_id
        self.base_id = base_id
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.min_price = min_price
        self.max_price = max_price
        self.sell_mode = sell_mode

    def __repr__(self):
        return f"<EventModel(id={self.id}, title={self.title}, start_date={self.start_date}, end_date={self.end_date}, min_price={self.min_price}, max_price={self.max_price}, sell_mode={self.sell_mode})>"
