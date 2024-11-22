from flask import request
from flask_restx import Namespace, Resource, fields
from app.data import destinations, save_destinations
from config import Config
import jwt


SECRET_KEY = Config.JWT_SECRET_KEY

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


def is_admin():
    """
    Check if the user has admin privileges by validating the JWT token.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        print("Authorization header missing or invalid")  # Debugging
        return False

    token = auth_header.split(" ")[1]  # Extract the token after "Bearer"
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("Decoded token payload:", payload)  # Debugging
        # Check if the user role is admin
        return payload.get("role") == "Admin"
    except jwt.ExpiredSignatureError:
        print("Token expired")  # Debugging
        return False
    except jwt.InvalidTokenError:
        print("Invalid token")  # Debugging
        return False


@destination_ns.route("/")
class DestinationList(Resource):
    @destination_ns.doc("list_destinations")
    @destination_ns.marshal_list_with(destination_model)
    def get(self):
        """Retrieve a list of all travel destinations."""
        return destinations, 200

    @destination_ns.doc(
        "create_destination",
        security="Bearer",  # Requires Bearer token
        responses={
            201: "Created",
            400: "Invalid input",
            403: "Unauthorized access",
        },
    )
    @destination_ns.expect(destination_model, validate=True)
    def post(self):
        """Create a new travel destination (Admin-only)."""
        if not is_admin():
            return {"message": "Unauthorized access. Admins only!"}, 403

        # Parse the input data
        data = request.json
        new_id = max(d["id"] for d in destinations) + 1 if destinations else 1

        # Create the destination
        new_destination = {
            "id": new_id,
            "name": data["name"],
            "description": data["description"],
            "location": data["location"],
        }
        destinations.append(new_destination)
        save_destinations(destinations)
        return {
            "message": "Destination created successfully",
            "destination": new_destination,
        }, 201


@destination_ns.route("/<int:id>")
class Destination(Resource):
    @destination_ns.doc(
        "delete_destination",
        security="Bearer",  # Requires Bearer token
        params={"id": "The ID of the destination to delete"},
    )
    def delete(self, id):
        """Delete a specific travel destination (Admin-only)."""
        if not is_admin():
            return {"message": "Unauthorized access. Admins only!"}, 403

        global destinations
        destination = next((d for d in destinations if d["id"] == id), None)
        if not destination:
            return {"message": "Destination not found"}, 404

        destinations = [d for d in destinations if d["id"] != id]
        save_destinations(destinations)
        return {"message": "Destination deleted successfully"}, 200
