"""Event class"""
from abc import ABC, abstractmethod


class DomainEvent(ABC):
    """Domain Event class"""
    def __init__(self, aggregate_id: str, event_id: str, ocurred_on: str):
        self.aggregate_id = aggregate_id
        self.event_id = event_id
        self.ocurred_on = ocurred_on


    @classmethod
    @abstractmethod
    def event_name(cls) -> str:
        """Returns the event name"""
