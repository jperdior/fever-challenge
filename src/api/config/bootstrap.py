"""Configuration file for the API module"""

import os

from flask import Flask
from flasgger import Swagger
from flask_migrate import Migrate
from src.api.routes.events import events_routes
from src.api.routes.status import status_bp
from src.api.command.events import events_commands
from src.shared.infrastructure.persistence.postgresql import DB, SQLALCHEMY_DATABASE_URI
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
from src.contexts.events.infrastructure.bus.inmemory.query import QueryBusImpl
from src.contexts.events.infrastructure.bus.rabittmq.command import CommandBusImpl

POSTGRES_DB = os.getenv("POSTGRES_DB", "fever_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "fever_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "fever_pass")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", str(5432))

SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
if not CELERY_BROKER_URL:
    raise ValueError("CELERY_BROKER_URL is not set")



def create_app():
    """Run the API"""

    event_repository = EventRepositoryImpl(db=DB)
    event_cache = EventCache(cache=CACHE)

    query_bus = QueryBusImpl()
    command_bus = CommandBusImpl(celery_broker_url=CELERY_BROKER_URL)


    search_service = SearchService(repository=event_repository, cache=event_cache)
    search_controller = SearchController(query_bus=query_bus)
    query_bus.register(
        SearchEventsQuery.type(), SearchEventsQueryHandler(service=search_service)
    )

    challenge_provider = ChallengeProvider()
    fetch_service = FetchEventsService(provider=challenge_provider, command_bus=command_bus)

    parser = ChallengeEventParser()
    parse_and_create_service = ParseAndCreateService(
        repository=event_repository, parser=parser
    )
    command_bus.register(
        ParseAndCreateCommand, ParseAndCreateHandler(service=parse_and_create_service)
    )


    app = Flask(__name__)
    Swagger(app)

    app.register_blueprint(status_bp)
    app.register_blueprint(events_routes(search_controller))
    app.register_blueprint(events_commands(fetch_service))

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    DB.init_app(app)
    Migrate(app, DB)

    return app