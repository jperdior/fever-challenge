"""Routes for the events context."""
from flask import Blueprint, request, jsonify

from src.contexts.events.presentation.search import SearchController
from src.contexts.events.application.search.service import SearchService

# Create a Blueprint for your routes
events_bp = Blueprint("events", __name__)


@events_bp.route("/search", methods=["GET"])
def search():
    """Search events"""
    search_service = SearchService()
    events = SearchController(search_service=search_service).execute(request)
    return jsonify(events.to_dict())
