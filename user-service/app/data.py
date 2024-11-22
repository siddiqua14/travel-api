import os

# Path to the user data file
DATA_FILE = "user_data.py"


# Function to load users from user_data.py
def load_users_data():
    """Load users data from the data file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            content = file.read()
            try:
                # Execute the content to load users_data
                local_vars = {}
                exec(
                    content, {}, local_vars
                )  # Use a local namespace to avoid pollution
                users_data = local_vars.get("users_data", [])
                if not isinstance(users_data, list):
                    raise ValueError(
                        "Invalid format in data file: users_data should be a list"
                    )
                return users_data
            except Exception as e:
                print(f"Error loading data: {e}")
                return []  # Return an empty list in case of an error
    else:
        return []  # Return an empty list if the file doesn't exist


# Function to save users to user_data.py
def save_users_data(new_users):
    """
    Append new users to the existing users_data in the data file.

    :param new_users: List of new users to append to the data file.
    """
    # Load existing users
    existing_users = load_users_data()

    # Append new users
    updated_users = existing_users + new_users

    # Write the updated users_data back to the file
    with open(DATA_FILE, "w") as file:
        file.write(f"users_data = {repr(updated_users)}")
