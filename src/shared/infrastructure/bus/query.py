"""Query bus interfaces"""

from abc import ABC, abstractmethod
from typing import Any


class Query(ABC):
    """Query interface"""

    @abstractmethod
    def type(self) -> str:
        """Query type"""


class Handler(ABC):
    """Query handler interface"""

    @abstractmethod
    def handle(self, query: Query) -> Any:
        """Handle a query"""


class QueryBus(ABC):
    """Query bus interface"""

    @abstractmethod
    def ask(self, query: Query) -> Any:
        """Ask a query"""

    @abstractmethod
    def register(self, query_type: str, handler: Handler) -> None:
        """Register a query handler"""
