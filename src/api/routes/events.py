from flask import Blueprint, request

from src.contexts.events.presentation.search import SearchController

# Create a Blueprint for your routes
events_bp = Blueprint('events', __name__)

@events_bp.route('/search', methods=['GET'])
def search():
    events = SearchController().execute(request)
    return events