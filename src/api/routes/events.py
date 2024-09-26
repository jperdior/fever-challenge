"""Routes for the events context."""

from flask import Blueprint, request, jsonify
from src.api.config.config import search_controller

# Create a Blueprint for your routes
events_bp = Blueprint("events-router", __name__)


@events_bp.route("/search", methods=["GET"])
def search():
    """Search events"""
    events = search_controller.execute(request)
    return jsonify(events.to_dict())
