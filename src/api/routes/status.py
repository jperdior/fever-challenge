"""Status route"""

from flask import Blueprint

# Create a Blueprint for your routes
status_bp = Blueprint("status-router", __name__)


@status_bp.route("/status", methods=["GET"])
def status():
    """Status endpoint"""
    return "ok", 200
