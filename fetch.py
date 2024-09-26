"""Runs the Flask application."""
from flask import Flask
from src.api.command.events import events_commands_bp

app = Flask(__name__)
app.register_blueprint(events_commands_bp)


if __name__ == "__main__":
    app.run(debug=True)
