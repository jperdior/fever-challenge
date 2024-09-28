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
        format: date
        default: 2017-07-21T17:32:28Z
      - name: ends_at
        in: query
        type: string
        required: true
        description: Return only events that finishes before this date
        format: date-time
        default: 2021-07-21T17:32:28Z
    responses:
      200:
        description: List of plans
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                events:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                        default: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                      title:
                        type: string
                        default: "Event title"
                      start_date:
                        type: string
                      start_time:
                        type: string
                      end_date:
                        type: string
                      end_time:
                        type: string
                      min_price:
                        type: number
                      max_price:
                        type: number
            error:
              type: object
              nullable: true
              properties:
                code:
                  type: string
                message:
                  type: string
      400:
        description: Bad request
        schema:
          type: object
          properties:
            error:
              type: object
              properties:
                code:
                  type: string
                message:
                  type: string
            data:
                type: null
      500:
        description: Bad request
        schema:
          type: object
          properties:
            error:
              type: object
              properties:
                code:
                  type: string
                message:
                  type: string
                   
    """
    events = search_controller.execute(request)
    if events.error:
        return jsonify(events.error.to_dict()), events.error.code
    return jsonify(events.to_dict())
