from flask import request
from flask_restx import Namespace, Resource, fields
from app.data import destinations, save_data

destination_ns = Namespace("destinations", description="Manage travel destinations")

# Swagger model for destination details
destination_model = destination_ns.model(
    "Destination",
    {
        "id": fields.Integer(description="Unique ID"),
        "name": fields.String(required=True, description="Destination name"),
        "description": fields.String(required=True, description="Short description"),
        "location": fields.String(required=True, description="Location name"),
    },
)


# Helper function for role-based access
def is_admin():
    auth_header = request.headers.get("Authorization", "")
    return auth_header == "Bearer admin-token"  # Replace with real token validation!


@destination_ns.route("/")
class DestinationList(Resource):
    @destination_ns.doc("list_destinations")
    @destination_ns.marshal_list_with(destination_model)
    def get(self):
        """Retrieve a list of all travel destinations."""
        return destinations, 200


@destination_ns.route("/<int:id>")
class Destination(Resource):
    @destination_ns.doc("delete_destination", security="Bearer")
    def delete(self, id):
        """Delete a specific travel destination (Admin-only)."""
        if not is_admin():
            return {"message": "Unauthorized access. Admins only!"}, 403

        global destinations
        destination = next((d for d in destinations if d["id"] == id), None)
        if not destination:
            return {"message": "Destination not found"}, 404

        destinations = [d for d in destinations if d["id"] != id]
        save_data(destinations)
        return {"message": "Destination deleted successfully"}, 200
