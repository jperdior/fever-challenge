"""Events routes"""
from flask import Blueprint, request, jsonify
from src.contexts.events.presentation.search import SearchController

def events_routes(search_controller: SearchController):
    """Events routes"""
    events_routes_bp = Blueprint("events-router", __name__)

    @events_routes_bp.route("/search", methods=["GET"])
    def search():
        """Search events
        ---
        parameters:
          - name: starts_at
            in: query
            type: string
            required: true
            description: Return only events that start after this date
            default: 2017-07-21T17:32:28Z
          - name: ends_at
            in: query
            type: string
            required: true
            description: Return only events that end before this date
            default: 2021-07-21T17:32:28Z
        definitions:
          EventList:
            type: array
            name: events
            items:
              $ref: '#/definitions/EventSummary'
          EventSummary:
            type: object
            properties:
              id:
                type: string($uuid)
                description: Identifier for the plan (UUID)
                example: 3fa85f64-5717-4562-b3fc-2c963f66afa6
              title:
                type: string
                description: Title of the plan
              start_date:
                type: string($date)
                description: Date when the event starts in local time
                example: 2021-07-21
              start_time:
                type: string($time)
                nullable: true
                example: 20:00:00
                description: Time when the event starts in local time
              end_date:
                type: string($date)
                description: Date when the event ends in local time
                example: 2021-07-21
              end_time:
                type: string($time)
                nullable: true
                example: 22:00:00
                description: Time when the event ends in local time
              min_price:
                type: number
                nullable: true
              max_price:
                type: number
                nullable: true
        responses:
          200:
            description: List of plans
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    $ref: '#/definitions/EventSummary'
                error:
                  type: object
                  nullable: true
                  properties:
                    code:
                      type: integer
                    message:
                      type: string

          400:
            description: Bad request
          500:
            description: Internal server error
        """
        result = search_controller.execute(request)
        if result.error:
            return jsonify(result.to_dict()), result.error.code
        return jsonify(result.to_dict())

    return events_routes_bp
