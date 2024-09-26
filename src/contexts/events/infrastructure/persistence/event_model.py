"""Event model module"""
from sqlalchemy import Column, Integer, String, DateTime, Float, func
from src.shared.infrastructure.persistence.postgresql import Base


class EventModel(Base):
    """Event model class"""
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    min_price = Column(Float)
    max_price = Column(Float)
    created_at = Column(DateTime, default=func.now)
    updated_at = Column(DateTime, default=func.now)
    deleted_at = Column(DateTime, default=None)
