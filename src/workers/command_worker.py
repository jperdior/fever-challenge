from celery import Celery
from src.api.config.bootstrap import create_command_celery_app
from src.shared.domain.bus.command import CommandBus, Command
from src.shared.infrastructure.bus.rabittmq.command import CommandBusImpl

# Define your Celery app
command_celery_app = create_command_celery_app()

# Create an instance of CommandBusImpl
command_bus = CommandBusImpl(celery_app=command_celery_app)

# Register your command handlers
def register_handlers():
    # Replace SomeCommand with your actual command classes
    command_bus.register(SomeCommand, SomeCommandHandler())
    # Add more handlers as necessary

# Register handlers when the worker starts
register_handlers()

if __name__ == "__main__":
    # Start the Celery worker with the command bus app
    command_celery_app.start()
