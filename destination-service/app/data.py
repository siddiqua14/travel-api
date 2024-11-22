# This file stores and manages destination data in Python format

# Sample destination data
destinations = [
    {
        "id": 1,
        "name": "Paris",
        "description": "The city of lights.",
        "location": "France",
    },
    {
        "id": 2,
        "name": "Tokyo",
        "description": "A bustling metropolis.",
        "location": "Japan",
    },
]


def save_data(data):
    """
    Save the given data back into this Python file.
    """
    with open(__file__, "w") as file:
        file.write(
            "# This file stores and manages destination data in Python format\n\n"
        )
        file.write(f"destinations = {repr(data)}\n")
