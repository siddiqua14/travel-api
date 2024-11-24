from flask import Flask, redirect
from flask_restx import Api
from flasgger import Swagger
from app.auth import auth_api
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize API
    authorizations = {
        "Bearer Auth": {"type": "apiKey", "in": "header", "name": "Authorization"}
    }

    api = Api(
        app,
        version="1.0",
        title="Authentication Service API",
        description="Manages authentication and role-based access",
        doc="/",
        authorizations=authorizations,
        security="Bearer Auth",
    )

    Swagger(app)  # Swagger UI for documentation

    @app.route("/")
    def home():
        return redirect("/swagger/")

    api.add_namespace(auth_api)  # Register the auth namespace
    return app
