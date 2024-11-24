from flask import Flask
from flask_restx import Api
from flask_cors import CORS  # Import Flask-CORS
from app.destination import destination_ns


def create_app():
    app = Flask(__name__)

    # Enable CORS for the app
    CORS(app)

    # Allow URLs with and without trailing slashes
    app.url_map.strict_slashes = False

    # Define Bearer token security scheme
    authorizations = {
        "Bearer": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter your bearer token like this: Bearer <token>",
        }
    }

    # Initialize API with security settings
    api = Api(
        app,
        version="1.0",
        title="Destination Service API",
        description="API for managing travel destinations",
        doc="/",
        security="Bearer",  # Apply Bearer security globally
        authorizations=authorizations,  # Include the authorizations in Swagger
    )

    # Add the destinations namespace
    api.add_namespace(destination_ns, path="/destinations")

    return app
