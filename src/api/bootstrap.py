"""Bootstrap file file for the API"""

import os

from flask import Flask
from flasgger import Swagger
from flask_migrate import Migrate
from celery import Celery, Task
from src.api.routes.events import events_routes
from src.api.routes.status import status_bp
from src.api.command.events import events_commands
from src.shared.infrastructure.persistence.postgresql import DB, SQLALCHEMY_DATABASE_URI

# importing for migrations
from src.contexts.events.infrastructure.persistence.event_model import EventModel

from src.contexts.events.application.parse_and_create.command import (
    ParseAndCreateCommand,
    ParseAndCreateHandler,
)
from src.contexts.events.infrastructure.cache.event_cache import EventCache
from src.contexts.events.infrastructure.persistence.event_repository import (
    EventRepositoryImpl,
)
from src.contexts.events.presentation.search import SearchController
from src.contexts.events.application.search.service import SearchService
from src.contexts.events.application.search.query import (
    SearchEventsQuery,
    SearchEventsQueryHandler,
)
from src.contexts.events.infrastructure.providers.challenge_provider import (
    ChallengeProvider,
    ChallengeEventParser,
)
from src.contexts.events.application.fetch.service import FetchEventsService
from src.contexts.events.application.parse_and_create.service import (
    ParseAndCreateService,
)
from src.shared.infrastructure.cache.redis import CACHE
from src.shared.infrastructure.bus.inmemory.query import QueryBusImpl
from src.shared.infrastructure.bus.rabittmq.command import CommandBusImpl

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
if not CELERY_BROKER_URL:
    raise ValueError("CELERY_BROKER_URL is not set")


def celery_init_command(app: Flask) -> Celery:
    """Initialize the Celery app"""

    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery("command_bus", task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["CELERY"] = celery_app
    return celery_app


def create_app():
    """Run the API"""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    DB.init_app(app)
    Migrate(app, DB)

    app.config["CELERY"] = {"broker_url": CELERY_BROKER_URL, "task_ignore_result": True}
    app.config.from_prefixed_env()
    command_celery_app = celery_init_command(app)

    event_repository = EventRepositoryImpl(db=DB)
    event_cache = EventCache(cache=CACHE)

    challenge_provider = ChallengeProvider()
    parser = ChallengeEventParser()

    query_bus = QueryBusImpl()
    command_bus = CommandBusImpl(celery_app=command_celery_app)

    search_controller = SearchController(query_bus=query_bus)

    search_service = SearchService(repository=event_repository, cache=event_cache)
    fetch_service = FetchEventsService(
        provider=challenge_provider, command_bus=command_bus
    )
    parse_and_create_service = ParseAndCreateService(
        repository=event_repository, parser=parser
    )

    query_bus.register(
        SearchEventsQuery.type(), SearchEventsQueryHandler(service=search_service)
    )

    command_bus.register(
        ParseAndCreateCommand, ParseAndCreateHandler(service=parse_and_create_service)
    )

    Swagger(app)

    app.register_blueprint(status_bp)
    app.register_blueprint(events_routes(search_controller))
    app.register_blueprint(events_commands(fetch_service))

    return app
