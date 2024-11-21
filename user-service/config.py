import os


class Config:
    SECRET_KEY = os.urandom(24)  # Secret key for JWT token encryption
    JWT_SECRET_KEY = "your_jwt_secret"  # Secret key for JWT token encoding
    JWT_ACCESS_TOKEN_EXPIRES = 3600
