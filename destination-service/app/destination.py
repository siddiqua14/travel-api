from flask_restx import Namespace, Resource, fields
from flask import request

# Define the API namespace
destination_api = Namespace(
    "destinations", description="Destination related operations"
)

destination_model = destination_api.model(
    "Destination",
    {
        "id": fields.Integer(
            readonly=True, description="The destination unique identifier"
        ),
        "name": fields.String(
            required=True, description="The name of the destination"
        ),
        "description": fields.String(
            required=True, description="A brief description of the destination"
        ),
        "location": fields.String(
            required=True, description="The location of the destination"
        ),
    },
)

# In-memory destination data
destinations = []  # This list will hold the destination data in-memory


# Destination Resource (GET and POST endpoints)
@destination_api.route("/")
class DestinationList(Resource):
    @destination_api.doc("list_destinations")
    @destination_api.marshal_list_with(destination_model)
    def get(self):
        """List all destinations"""
        return destinations

    @destination_api.doc("create_destination")
    @destination_api.expect(destination_model)
    @destination_api.marshal_with(destination_model, code=201)
    def post(self):
        """Create a new destination"""
        new_dest = request.json  # Get the new destination data from request
        new_dest["id"] = len(destinations) + 1  # Assign a new ID
        destinations.append(new_dest)  # Append to the destinations list
        return new_dest, 201


# Destination Resource (DELETE endpoint by ID)
@destination_api.route("/<int:id>")
@destination_api.param("id", "The destination identifier")
class Destination(Resource):
    @destination_api.doc("delete_destination")
    def delete(self, id):
        """Delete a destination by its ID"""
        global destinations
        destinations = [dest for dest in destinations if dest["id"] != id]
        return "", 204
