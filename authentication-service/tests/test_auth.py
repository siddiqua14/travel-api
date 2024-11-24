import unittest
from unittest.mock import patch
from app import create_app
import jwt
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from config import Config


class AuthServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up Flask test client."""
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app.testing = True
        cls.valid_user = {
            "id": 1,
            "email": "testuser@example.com",
            "password": generate_password_hash("password123"),  # Mocked hashed password
            "role": "User",
        }
        cls.admin_user = {
            "id": 2,
            "email": "admin@example.com",
            "password": generate_password_hash("admin123"),  # Mocked hashed password
            "role": "Admin",
        }

    def generate_token(self, user):
        """Helper function to generate a valid JWT token."""
        expiration = datetime.utcnow() + timedelta(hours=1)
        token = jwt.encode(
            {"user_id": user["id"], "role": user["role"], "exp": expiration},
            Config.JWT_SECRET_KEY,
            algorithm="HS256",
        )
        return token

    @patch("auth.fetch_user_data")
    def test_login_success(self, mock_fetch_user):
        """Test successful login and token generation."""
        mock_fetch_user.return_value = self.valid_user  # Use valid_user setup

        response = self.client.post(
            "/auth/login",
            json={"email": "testuser@example.com", "password": "password123"},
        )
        self.assertEqual(response.status_code, 200)  # Ensure the response is successful
        data = response.get_json()
        self.assertIn("token", data)  # Validate token presence in response

    @patch("auth.fetch_user_data")
    def test_login_invalid_password(self, mock_fetch_user):
        """Test login with invalid password."""
        mock_fetch_user.return_value = self.valid_user
        response = self.client.post(
            "/auth/login",
            json={"email": "testuser@example.com", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid email or password", response.get_json()["message"])

    @patch("auth.fetch_user_data")
    def test_login_user_not_found(self, mock_fetch_user):
        """Test login when user is not found."""
        mock_fetch_user.return_value = None
        response = self.client.post(
            "/auth/login",
            json={"email": "notfound@example.com", "password": "password123"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid email or password", response.get_json()["message"])

    def test_validate_token_success(self):
        """Test validating a valid token."""
        token = self.generate_token(self.valid_user)
        response = self.client.get(
            "/auth/validate",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Token is valid", response.get_json()["message"])

    def test_validate_token_expired(self):
        """Test validating an expired token."""
        expiration = datetime.utcnow() - timedelta(hours=1)  # Token expired
        expired_token = jwt.encode(
            {
                "user_id": self.valid_user["id"],
                "role": self.valid_user["role"],
                "exp": expiration,
            },
            Config.JWT_SECRET_KEY,
            algorithm="HS256",
        )
        response = self.client.get(
            "/auth/validate",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("Token expired", response.get_json()["message"])

    def test_admin_access_success(self):
        """Test accessing admin-only route with valid admin token."""
        token = self.generate_token(self.admin_user)
        response = self.client.get(
            "/auth/admin-access",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Welcome, Admin!", response.get_json()["message"])

    def test_admin_access_unauthorized(self):
        """Test accessing admin-only route with non-admin token."""
        token = self.generate_token(self.valid_user)
        response = self.client.get(
            "/auth/admin-access",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn("Access denied. Admins only.", response.get_json()["message"])

    def test_admin_access_invalid_token(self):
        """Test accessing admin-only route with invalid token."""
        response = self.client.get(
            "/auth/admin-access",
            headers={"Authorization": "Bearer invalidtoken"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid token", response.get_json()["message"])


if __name__ == "__main__":
    unittest.main()
