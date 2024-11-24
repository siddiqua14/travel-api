from datetime import datetime, timedelta
import unittest
from app import create_app
from app.data import save_destinations, load_destinations
import jwt
from config import Config


class DestinationServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the Flask test client and sample data."""
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app.testing = True

        cls.test_destination = {
            "name": "Paris",
            "description": "City of Light",
            "location": "France",
            "id": 9999,  # Unique ID
        }

        # Load existing data and append test-specific data
        cls.original_data = load_destinations()
        save_destinations(cls.original_data + [cls.test_destination])

    @classmethod
    def tearDownClass(cls):
        """Clean up only test-specific data."""
        current_data = load_destinations()
        filtered_data = [
            dest for dest in current_data if dest["id"] != cls.test_destination["id"]
        ]
        save_destinations(filtered_data)

    @classmethod
    def authenticate_admin(cls):
        """
        Generate a valid admin token.
        """
        payload = {
            "role": "Admin",
            "exp": datetime.utcnow() + timedelta(hours=1),  # Token expiration
        }
        token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")
        return token

    def test_create_destination_success(self):
        """Test creating a new destination."""
        token = self.authenticate_admin()  # Generate admin token
        new_destination = {
            "name": "Tokyo",
            "description": "City of the Rising Sun",
            "location": "Japan",
        }
        response = self.client.post(
            "/destinations",
            json=new_destination,
            headers={"Authorization": f"Bearer {token}"},  # Use the token here
        )
        self.assertEqual(response.status_code, 201)

    def test_get_all_destinations(self):
        """Test retrieving all destinations."""
        response = self.client.get("/destinations")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)  # At least 1 destination exists

    def test_delete_destination_success(self):
        """Test deleting an existing destination."""
        # Authenticate as admin to get a valid token
        token = self.authenticate_admin()

        # Add a test destination to delete
        test_destination = {
            "id": 999,  # Unique ID for this test
            "name": "Test Destination",
            "description": "A destination for testing",
            "location": "Testland",
        }
        # Add to destinations
        save_destinations(load_destinations() + [test_destination])
        print(load_destinations())  # Debug: Check if the test destination is present

        # Send DELETE request
        response = self.client.delete(
            f"/destinations/{test_destination['id']}",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn("Destination deleted successfully", response.json["message"])

        # Verify the destination is no longer in the list
        remaining_destinations = load_destinations()
        self.assertFalse(any(d["id"] == test_destination["id"] for d in remaining_destinations))

    def test_delete_destination_unauthorized(self):
        """Test deleting a destination without admin privileges."""
        # Attempt to delete without an admin token
        response = self.client.delete("/destinations/1")

        # Assertions
        self.assertEqual(response.status_code, 403)
        self.assertIn("Unauthorized access", response.json["message"])

    def test_delete_destination_not_found(self):
        """Test deleting a destination that does not exist."""
        # Authenticate as admin to get a valid token
        token = self.authenticate_admin()

        # Send DELETE request for a non-existent destination
        response = self.client.delete(
            "/destinations/99999",  # ID not present in destinations
            headers={"Authorization": f"Bearer {token}"}
        )

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.assertIn("Destination not found", response.json["message"])


if __name__ == "__main__":
    unittest.main()
