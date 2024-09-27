"""Runs the Flask application."""
from flask import Flask
from flasgger import Swagger
from flask_migrate import Migrate
from src.api.routes.events import events_bp
from src.api.command.events import events_commands_bp
from src.shared.infrastructure.persistence.postgresql import DB, SQLALCHEMY_DATABASE_URI
from src.contexts.events.infrastructure.persistence.event_model import EventModel

app = Flask(__name__)
swagger = Swagger(app)
app.register_blueprint(events_bp)
app.register_blueprint(events_commands_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
DB.init_app(app)
migrate = Migrate(app, DB)

if __name__ == "__main__":
    app.run(debug=True)
