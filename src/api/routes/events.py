"""Routes for the events context."""

from flask import Blueprint, request, jsonify
from src.api.config.config import search_controller

# Create a Blueprint for your routes
events_bp = Blueprint("events-router", __name__)


@events_bp.route("/search", methods=["GET"])
def search():
    """Search events
    
    ---
    tags:
      - Events
    parameters:
      - name: starts_at
        in: query
        type: string
        required: true
        description: Return only events that starts after this date
        x-example: 2017-07-21T17:32:28Z
      - name: ends_at
        in: query
        type: string
        required: true
        description: Return only events that finishes before this date
        x-example: 2021-07-21T17:32:28Z
    responses:
      200:
        description: A list of events
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  name:
                    type: string
                  starts_at:
                    type: string
                  ends_at:
                    type: string
            error:
              type: object
              properties:
                message:
                  type: string
                code:
                  type: integer
      400:
        description: Bad request
        schema:
          type: object
          properties:
            error:
              type: object
              properties:
                message:
                  type: string
                code:
                  type: integer
    """
    events = search_controller.execute(request)
    return jsonify(events.to_dict()), events.error.code
