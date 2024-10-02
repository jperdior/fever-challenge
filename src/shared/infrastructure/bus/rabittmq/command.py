# src/shared/infrastructure/bus/command.py

import json
from typing import Dict, Type
from celery import Celery
from src.shared.domain.bus.command import CommandBus, Command, Handler


class CommandBusImpl(CommandBus):
    """Celery command bus implementation"""

    def __init__(self, celery_app: Celery):
        # Initialize Celery app
        self.celery_app = celery_app
        self.handlers: Dict[str, Handler] = {}

    def dispatch(self, command: Command) -> None:
        """Dispatch a command"""
        command_type = type(command).__name__
        if command_type not in self.handlers:
            raise ValueError(f"No handler registered for command type '{command_type}'")
        command_data = json.dumps(command.__dict__)

        self.celery_app.send_task(command_type, args=[command_data])

    def register(self, command_type: Type[Command], handler: Handler) -> None:
        """Register a command handler"""
        command_type_name = command_type.__name__
        self.handlers[command_type_name] = handler

        @self.celery_app.task(name=command_type_name)
        def task(command_json: str):
            command_dict = json.loads(command_json)
            command_instance = command_type(**command_dict)
            handler.handle(command_instance)
