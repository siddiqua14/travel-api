import os

# Path to the destination data file
DESTINATION_FILE = "destination_data.py"


# Function to load destinations from the data file
def load_destinations():
    """Load destination data from the data file."""
    if os.path.exists(DESTINATION_FILE):
        with open(DESTINATION_FILE, "r") as file:
            content = file.read()
            try:
                # Execute the content to load destinations
                local_vars = {}
                exec(
                    content, {}, local_vars
                )  # Use a local namespace to avoid pollution
                destinations = local_vars.get("destinations", [])
                if not isinstance(destinations, list):
                    raise ValueError(
                        "Invalid format in data file: destinations should be a list"
                    )
                return destinations
            except Exception as e:
                print(f"Error loading destinations: {e}")
                return []  # Return an empty list in case of an error
    else:
        return []  # Return an empty list if the file doesn't exist


# Function to save destinations to the data file
def save_destinations(updated_destinations):
    """
    Save the updated destinations list to the data file.

    :param updated_destinations: List of updated destinations to save.
    """
    with open(DESTINATION_FILE, "w") as file:
        file.write(f"destinations = {repr(updated_destinations)}")


# Initialize destinations with data from the file
destinations = load_destinations()
