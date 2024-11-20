# __init__.py

from flask import Flask
from flask_restx import Api
from flask_restful import Resource, Api
from apispec import APISpec
from .destination import destination_api
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs

from API.Destinations.destinations import DestninationList


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    api = Api(
        app,
        version="1.0",
        title="Travel API",
        description="A simple Travel API for destinations",
    )

    # Register the destination API namespace
    api.add_namespace(destination_api)

    return app
