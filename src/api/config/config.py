"""Configuration file for the API module"""

from src.contexts.events.infrastructure.cache.event_cache import EventCache
from src.contexts.events.infrastructure.persistence.event_repository import (
    EventRepositoryImpl,
)
from src.contexts.events.presentation.search import SearchController
from src.contexts.events.application.search.service import SearchService
from src.contexts.events.infrastructure.providers.challenge_provider import (
    ChallengeProvider,
)
from src.contexts.events.application.fetch.service import FetchEventsService
from src.shared.infrastructure.persistence.postgresql import DB
from src.shared.infrastructure.cache.redis import CACHE


event_repository = EventRepositoryImpl(db=DB)
event_cache = EventCache(cache=CACHE)

search_service = SearchService(repository=event_repository,cache=event_cache)
search_controller = SearchController(search_service=search_service)

challenge_provider = ChallengeProvider()
fetch_service = FetchEventsService(
    provider=challenge_provider, repository=event_repository
)
