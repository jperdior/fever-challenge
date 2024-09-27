#!/bin/bash

# Navigate to the project directory
cd /app

# Run the database migrations
poetry run flask db upgrade

# Run the Flask application
poetry run flask run --host=0.0.0.0 --port=5000

