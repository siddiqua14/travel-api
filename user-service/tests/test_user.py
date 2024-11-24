import unittest
from app import create_app
from app.data import save_users_data
from werkzeug.security import generate_password_hash


class UserServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the Flask test client and sample data."""
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app.testing = True

        # Prepare initial test data
        cls.test_user = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": generate_password_hash("password123"),
            "role": "User",
            "id": 1,
        }
        save_users_data([cls.test_user])  # Save initial test user

    @classmethod
    def tearDownClass(cls):
        """Clean up the data file after tests."""
        save_users_data([])  # Clear user data

    def authenticate_user(self):
        """Helper method to authenticate a user and return a JWT token."""
        response = self.client.post(
            "/users/login",
            json={"email": self.test_user["email"], "password": "password123"},
        )
        if response.status_code == 200 and "token" in response.json:
            return response.json["token"]
        self.fail("Authentication failed. Could not retrieve token.")

    def test_register_user_success(self):
        """Test successful user registration."""
        response = self.client.post(
            "/users/register",
            json={
                "name": "New User",
                "email": "newuser@example.com",
                "password": "newpassword123",
                "role": "User",
            },
        )
        # Debugging information
        print(
            "Register request data:",
            {
                "name": "New User",
                "email": "newuser@example.com",
                "password": "newpassword123",
                "role": "User",
            },
        )
        print("Register response status:", response.status_code)
        print("Register response JSON:", response.json)

        self.assertEqual(response.status_code, 201)
        self.assertIn("email", response.json)
        self.assertEqual(response.json["email"], "newuser@example.com")

    def test_register_user_duplicate_email(self):
        """Test registration with an existing email."""
        response = self.client.post(
            "/users/register",
            json={
                "name": "Duplicate User",
                "email": "testuser@example.com",  # Same as test_user
                "password": "anotherpassword",
                "role": "User",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["message"], "Email already exists")

    def test_login_success(self):
        """Test successful login."""
        response = self.client.post(
            "/users/login",
            json={"email": "testuser@example.com", "password": "password123"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post(
            "/users/login",
            json={"email": "testuser@example.com", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json["message"], "Invalid credentials")

    def test_profile_access_success(self):
        """Test user profile retrieval with a valid token."""
        # Ensure token contains correct user data
        token = self.authenticate_user()

        response = self.client.get(
            "/users/profile",
            headers={"Authorization": f"Bearer {token}"},
        )
        # Debugging information
        print("Profile request headers:", {"Authorization": f"Bearer {token}"})
        print("Profile response status:", response.status_code)
        print("Profile response JSON:", response.json)

        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.json)
        self.assertEqual(response.json["email"], self.test_user["email"])

    def test_admin_access_success(self):
        """Test accessing admin route as an admin."""
        # Create an admin user and login
        admin_user = {
            "name": "Admin User",
            "email": "admin@example.com",
            "password": generate_password_hash("adminpassword"),
            "role": "Admin",
            "id": 2,
        }
        save_users_data([self.test_user, admin_user])

        login_response = self.client.post(
            "/users/login",
            json={"email": "admin@example.com", "password": "adminpassword"},
        )
        token = login_response.json["token"]

        response = self.client.get("/users/admin", headers={"Authorization": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Welcome Admin")

    def test_admin_access_forbidden(self):
        """Test accessing admin route as a non-admin."""
        login_response = self.client.post(
            "/users/login",
            json={"email": "testuser@example.com", "password": "password123"},
        )
        token = login_response.json["token"]

        response = self.client.get("/users/admin", headers={"Authorization": token})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json["message"], "Access denied. Admins only.")

    def test_admin_access_missing_token(self):
        """Test accessing admin route without a token."""
        response = self.client.get("/users/admin")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json["message"], "Token is missing")


if __name__ == "__main__":
    unittest.main()
