from flask import Flask, redirect
from flask_restx import Api
from flasgger import Swagger
from .user import user_api
from config import Config
import logging
logging.basicConfig(level=logging.DEBUG)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configure API with security definitions
    authorizations = {
        "Bearer Auth": {
            "type": "apiKey", "in": "header", "name": "Authorization"
        }
    }

    api = Api(
        app,
        version="1.0",
        title="User Service API",
        description="User registration, authentication, profile management",
        doc="/swagger/",
        authorizations=authorizations,
        security="Bearer Auth",
    )

    # Initialize Swagger UI
    Swagger(app)  # Initialize Flasgger for Swagger UI

    # Redirect root to Swagger UI
    @app.route("/")
    def home():
        """Redirect to Swagger UI"""
        return redirect("/swagger/")

    # Add the user API namespace
    api.add_namespace(user_api)

    return app
