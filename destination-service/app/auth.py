from functools import wraps
from flask import request, jsonify
import jwt

# Secret key to decode the token (this should be the same as the one used to encode the token)
SECRET_KEY = "your_secret_key_here"  # Replace with your actual secret key


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get(
            "Authorization"
        )  # Get token from Authorization header
        if not token:
            return jsonify({"message": "Unauthorized"}), 401

        try:
            # Decode and validate the token
            token = token.split(" ")[1]  # Remove "Bearer" part
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            if (
                decoded_token["sub"] != "admin_username"
            ):  # Check if the user is an admin
                return jsonify({"message": "Unauthorized"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function
