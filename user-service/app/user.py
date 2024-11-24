from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from app.data import save_users_data, load_users_data

user_api = Namespace(
    "users", description="User registration, authentication, profile management"
)

# Define user registration model for Swagger
user_model = user_api.model(
    "User",
    {
        "name": fields.String(required=True, description="Full name of the user"),
        "email": fields.String(required=True, description="Email address of the user"),
        "password": fields.String(required=True, description="Password of the user"),
        "role": fields.String(
            required=True, description="Role of the user, either 'Admin' or 'User'"
        ),
    },
)

# Define login model for Swagger
login_model = user_api.model(
    "Login",
    {
        "email": fields.String(required=True, description="Email address of the user"),
        "password": fields.String(required=True, description="Password of the user"),
    },
)


# Helper function to generate JWT token
def generate_token(user):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode(
        {"user_id": user["id"], "role": user["role"], "exp": expiration},
        Config.JWT_SECRET_KEY,
        algorithm="HS256",
    )
    return token


@user_api.route("/find")
class FindUser(Resource):
    @user_api.param("email", "User's email address", _in="query")
    def get(self):
        """Fetch a user by email"""
        email = request.args.get("email")
        users = load_users_data()
        user = next((u for u in users if u["email"] == email), None)
        if user:
            return user, 200
        return {"message": "User not found"}, 404


@user_api.route("/register")
class Register(Resource):
    @user_api.doc("register_user")
    @user_api.expect(user_model)
    def post(self):
        """Register a new user"""
        users_data = load_users_data()  # Load the latest users
        user_data = request.json

        # Check if the email already exists
        if any(user["email"] == user_data["email"] for user in users_data):
            return {"message": "Email already exists"}, 400

        # Assign a unique ID
        user_data["id"] = len(users_data) + 1
        user_data["password"] = generate_password_hash(user_data["password"])

        # Save the new user
        save_users_data([user_data])  # Pass as a list to append
        return user_data, 201


@user_api.route("/login")
class Login(Resource):
    @user_api.doc("login_user")
    @user_api.expect(login_model)
    def post(self):
        """Login a user and provide a JWT token"""
        users_data = load_users_data()  # Load the latest users
        login_data = request.json

        # Verify credentials
        for user in users_data:
            if user["email"] == login_data["email"] and check_password_hash(
                user["password"], login_data["password"]
            ):
                token = generate_token(user)
                return jsonify({"token": token})
        return {"message": "Invalid credentials"}, 401


@user_api.route("/profile")
class Profile(Resource):
    @user_api.doc("get_user_profile")
    @user_api.param("Authorization", "Bearer JWT Token", _in="header")
    def get(self):
        """Get user profile information (requires login)"""
        token = request.headers.get("Authorization")
        if not token:
            return {"message": "Token is missing"}, 401

        try:
            token_data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            user_id = token_data["user_id"]
            users_data = load_users_data()  # Load the latest users

            for user in users_data:
                if user["id"] == user_id:
                    return user, 200
            return {"message": "User not found"}, 404
        except jwt.ExpiredSignatureError:
            return {"message": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Invalid token"}, 401


@user_api.route("/admin")
class Admin(Resource):
    @user_api.doc("admin_only")
    @user_api.param("Authorization", "Bearer JWT Token", _in="header")
    def get(self):
        """Access for Admin users only"""
        token = request.headers.get("Authorization")
        if not token:
            return {"message": "Token is missing"}, 401

        try:
            token_data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            if token_data["role"] != "Admin":
                return {"message": "Access denied. Admins only."}, 403
            return {"message": "Welcome Admin"}, 200
        except jwt.ExpiredSignatureError:
            return {"message": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Invalid token"}, 401
