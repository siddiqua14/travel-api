import requests
from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from config import Config
import logging

# Initialize logger
logging.basicConfig(level=logging.DEBUG)

auth_api = Namespace("auth", description="Authentication and role-based access")

# Define Login model
login_model = auth_api.model(
    "Login",
    {
        "email": fields.String(required=True, description="User email"),
        "password": fields.String(required=True, description="User password"),
    },
)

# User Service endpoint
USER_SERVICE_URL = "http://localhost:5000/users/find"  # Adjust port if needed


def fetch_user_data(email):
    """Fetch user data from User Service"""
    try:
        response = requests.get(USER_SERVICE_URL, params={"email": email})
        if response.status_code == 200:
            user_data = response.json()
            logging.debug(f"Fetched user data: {user_data}")
            return user_data
        logging.error(f"User not found or bad response: {response.status_code}")
        return None
    except Exception as e:
        logging.error(f"Error fetching user data: {e}")
        return None


def generate_token(user):
    """Generate JWT token"""
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode(
        {
            "user_id": user["id"],
            "role": user["role"],
            "exp": expiration,
        },
        Config.JWT_SECRET_KEY,
        algorithm="HS256",
    )
    logging.debug(f"Generated token for user ID {user['id']}")
    return token


@auth_api.route("/login")
class Login(Resource):
    @auth_api.expect(login_model)
    def post(self):
        """User login and token generation"""
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and password are required"}, 400

        # Fetch user from User Service
        user = fetch_user_data(email)
        if not user:
            return {"message": "Invalid email or password"}, 401

        # Verify password
        if not check_password_hash(user["password"], password):
            logging.error(f"Invalid login attempt for email: {email}")
            return {"message": "Invalid email or password"}, 401

        # Generate token
        token = generate_token(user)
        return jsonify({"token": token})


@auth_api.route("/validate")
class ValidateToken(Resource):
    @auth_api.param("Authorization", "Bearer JWT Token", _in="header")
    def get(self):
        """Validate the provided JWT token"""
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            logging.error("Missing or invalid Authorization header")
            return {"message": "Token is missing or invalid"}, 401

        try:
            token = token.split(" ")[1]  # Extract the token part
            decoded = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            logging.debug(f"Decoded token: {decoded}")
            return {
                "message": "Token is valid",
                "user_id": decoded["user_id"],
                "role": decoded["role"],
            }, 200
        except jwt.ExpiredSignatureError:
            logging.error("Token has expired")
            return {"message": "Token expired"}, 401
        except jwt.InvalidTokenError:
            logging.error("Invalid token")
            return {"message": "Invalid token"}, 401


@auth_api.route("/admin-access")
class AdminAccess(Resource):
    @auth_api.param("Authorization", "Bearer JWT Token", _in="header")
    def get(self):
        """Restricted access for Admins"""
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return {"message": "Token is missing"}, 401

        try:
            # Decode token
            token = token.split(" ")[1]  # Extract the token part
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            logging.debug(f"Payload for Admin Access: {payload}")
            if payload["role"] != "Admin":
                return {"message": "Access denied. Admins only."}, 403
            return {"message": "Welcome, Admin!"}, 200
        except jwt.ExpiredSignatureError:
            logging.error("Token has expired")
            return {"message": "Token expired"}, 401
        except jwt.InvalidTokenError:
            logging.error("Invalid token")
            return {"message": "Invalid token"}, 401
