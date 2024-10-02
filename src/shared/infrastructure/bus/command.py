"""Command bus interfaces"""

from abc import ABC, abstractmethod
from typing import Any, Type


class Command(ABC):
    """Command interface"""

    @abstractmethod
    def type(self) -> str:
        """Command type"""


class Handler(ABC):
    """Command handler interface"""

    @abstractmethod
    def handle(self, command: Command) -> Any:
        """Handle a command"""


class CommandBus(ABC):
    """Query bus interface"""

    @abstractmethod
    def dispatch(self, command: Command) -> None:
        """Dispatch a command"""

    @abstractmethod
    def register(self, command_type: Type[Command], handler: Handler) -> None:
        """Register a command handler"""
