"""Aggregate Root module"""
from src.shared.domain.bus.event import DomainEvent


class AggregateRoot:
    """Aggregate Root class"""
    def __init__(self, aggregate_id: str):
        self.aggregate_id = aggregate_id
        self.events: list[DomainEvent] = []

    def record(self, event: DomainEvent):
        """Records a domain event in the aggregate"""
        self.events.append(event)

    def pull_events(self):
        """Pulls the domain events from the aggregate"""
        events = self.events
        self.events = []
        return events
