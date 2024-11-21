from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from app.data import users_data, save_users_data, load_users_data

# Load users data when the app starts#from config import Config
load_users_data()

user_api = Namespace(
    "users",
    description="User registration, authentication, profile management"
)

# Define user model for Swagger
user_model = user_api.model(
    "User",
    {
        "name": fields.String(
            required=True, description="Full name of the user"
            ),
        "email": fields.String(
            required=True, description="Email address of the user"
            ),
        "password": fields.String(
            required=True, description="Password of the user"
            ),
        "role": fields.String(
            required=True,
            description="Role of the user, either 'Admin' or 'User'"
        ),
    },
)


# Helper function to generate JWT token
def generate_token(user):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode(
        {"user_id": user["id"], "role": user["role"], "exp": expiration},
        "your_secret_key",  # Use actual secret key here
        algorithm="HS256",
    )
    return token


@user_api.route("/register")
class Register(Resource):
    @user_api.doc("register_user")
    @user_api.expect(user_model)
    def post(self):
        """Register a new user"""
        user_data = request.json

        # Check if the email already exists in the users_data
        for user in users_data:
            if user["email"] == user_data["email"]:
                return {"message": "Email already exists"}, 400

        # Assign unique ID based on the existing users' length
        user_data["id"] = len(users_data) + 1

        # Hash the password before saving
        user_data["password"] = generate_password_hash(user_data["password"])

        # Append the new user to the users_data list
        users_data.append(user_data)

        # Save the updated users data to file
        save_users_data()

        return user_data, 201


# User Resource (POST /login)
@user_api.route("/login")
class Login(Resource):
    @user_api.doc("login_user")
    @user_api.expect(user_model)
    def post(self):
        """Login a user and provide a JWT token"""
        login_data = request.json

        # Ensure both email and password are present
        if not login_data.get("email") or not login_data.get("password"):
            return {"message": "Email and password are required."}, 400

        for user in users_data:
            if user["email"] == login_data["email"] and check_password_hash(
                user["password"], login_data["password"]
            ):
                token = generate_token(user)
                return jsonify({"token": token})

        return {"message": "Invalid credentials"}, 401


# User Resource (GET /profile)
@user_api.route("/profile")
class Profile(Resource):
    @user_api.doc("get_user_profile")
    @user_api.param(
        "Authorization", "Bearer JWT Token", _in="header"
    )  # Documenting the Authorization header
    def get(self):
        """Get user profile information (requires login)"""
        token = request.headers.get("Authorization")
        if not token:
            return {"message": "Token is missing"}, 401

        try:
            token_data = jwt.decode(
                token, "your_secret_key", algorithms=["HS256"]
                )
            user_id = token_data["user_id"]
            for user in users_data:
                if user["id"] == user_id:
                    return user, 200
            return {"message": "User not found"}, 404
        except jwt.ExpiredSignatureError:
            return {"message": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Invalid token"}, 401


# Admin-only Resource (Access Control)
@user_api.route("/admin")
class Admin(Resource):
    @user_api.doc("admin_only")
    @user_api.param(
        "Authorization", "Bearer JWT Token", _in="header"
    )  # Documenting the Authorization header
    def get(self):
        """Access for Admin users only"""
        token = request.headers.get("Authorization")
        if not token:
            return {"message": "Token is missing"}, 401

        try:
            token_data = jwt.decode(
                token, "your_secret_key", algorithms=["HS256"]
            )
            if token_data["role"] != "Admin":
                return {"message": "Access denied. Admins only."}, 403
            return {"message": "Welcome Admin"}, 200
        except jwt.ExpiredSignatureError:
            return {"message": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Invalid token"}, 401
