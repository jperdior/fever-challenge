"""Runs the Flask application."""
from flask import Flask
from src.api.command.events import events_commands_bp
from src.shared.infrastructure.persistence.postgresql import DB, SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.register_blueprint(events_commands_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
DB.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
