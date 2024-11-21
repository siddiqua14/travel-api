# __init__.py

from flask import Flask
from flask_restx import Api
from .destination import destination_api


def create_app():
    # Create the Flask app
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize the API with Flask-RESTX
    api = Api(
        app,
        version="1.0",
        title="Travel API",
        description="A simple Travel API for destinations",
    )

    # Register the destination API namespace with the app
    api.add_namespace(destination_api)

    return app
