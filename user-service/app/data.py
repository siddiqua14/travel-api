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
            if content:
                exec(content)
            else:
                users_data = []
    else:
        users_data = []  # If file doesn't exist, initialize an empty list


# Function to save users to data file
def save_users_data():
    with open(DATA_FILE, "w") as file:
        file.write("users_data = " + repr(users_data))
