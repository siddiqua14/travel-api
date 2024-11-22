from flask import Flask
from flask_restx import Api
from app.destination import destination_ns


def create_app():
    app = Flask(__name__)

    # Set up Flask-RESTx API with Swagger documentation at /swagger/
    api = Api(
        app,
        version="1.0",
        title="Destination Service API",
        description="API for managing travel destinations",
        doc="/swagger/",  # Swagger UI available at /swagger/
    )

    # Add the destinations namespace
    api.add_namespace(destination_ns, path="/destinations")

    return app
