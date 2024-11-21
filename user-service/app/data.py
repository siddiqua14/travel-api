import os

# Path to data file
DATA_FILE = "data.py"

# Declare the users_data list at the module level
users_data = []


# Function to load users from data file
def load_users_data():
    global users_data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            content = file.read()
            try:
                exec(content)
            except Exception:
                users_data = []
    else:
        users_data = []  # If file doesn't exist, initialize an empty list


# Function to save users to data file
def save_users_data():
    global users_data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            # Read existing data and modify the `users_data` declaration
            existing_content = file.read()
            if "users_data =" in existing_content:
                # Replace the existing users_data content
                new_content = "users_data = " + repr(users_data)
            else:
                # If no `users_data` is present, start fresh
                new_content = "users_data = " + repr(users_data)
    else:
        # If file doesn't exist, create and write new data
        new_content = "users_data = " + repr(users_data)

    # Write to the file
    with open(DATA_FILE, "w") as file:
        file.write(new_content)
