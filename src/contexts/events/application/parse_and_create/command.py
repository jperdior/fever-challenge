"""Command to parse and create event"""

from src.shared.domain.bus.command import Command, Handler
from src.contexts.events.application.parse_and_create.service import (
    ParseAndCreateService,
)


class ParseAndCreateCommand(Command):
    """Parse and create command"""

    def __init__(self, event_data: str):
        self.event_data = event_data

    def type(self) -> str:
        return "ParseAndCreateCommand"


class ParseAndCreateHandler(Handler):
    """Command handler for ParseAndCreateCommand"""

    def __init__(self, service: ParseAndCreateService):
        self.service = service

    def handle(self, command: Command) -> None:
        """Handle a command"""
        if not isinstance(command, ParseAndCreateCommand):
            raise ValueError(f"Command '{command.type()}' not supported")
        self.service.execute(command.event_data)
