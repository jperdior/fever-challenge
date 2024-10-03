"""Cli commands for events."""

from flask import Blueprint
import click
from src.contexts.events.application.fetch.service import FetchEventsService


def events_commands(fetch_service: FetchEventsService):
    """Events commands"""

    events_commands_bp = Blueprint("events", __name__)

    @events_commands_bp.cli.command("fetch")
    def fetch_events():
        """Fetchs, parses and stores evenst from a provider"""
        click.echo("Here are the events...")
        fetch_service.execute()
        click.echo("Events fetched!")

    return events_commands_bp
