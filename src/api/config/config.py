"""Configuration file for the API module"""

from src.contexts.events.presentation.search import SearchController
from src.contexts.events.application.search.service import SearchService
from src.contexts.events.infrastructure.providers.challenge_provider import (
    ChallengeProvider,
)
from src.contexts.events.application.fetch.service import FetchEventsService

search_service = SearchService()
search_controller = SearchController(search_service=search_service)

challenge_provider = ChallengeProvider()
fetch_service = FetchEventsService(provider=challenge_provider)
