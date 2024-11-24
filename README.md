# Travel API with Microservices

This project implements a Travel API using a microservices architecture, ensuring scalability and separation of concerns. It provides services for managing users, destinations, and authentication.

## Project Structure

- **User Service**: Manages user data, including registration, authentication, and role management.
- **Destination Service**: Handles destinations with CRUD operations.
- **Authentication Service**: Provides JWT-based authentication and role-based access control.

## Technologies Used

- **Backend**: Flask, Flask-RESTx
- **Database**: SQLite (can be modified to other databases like PostgreSQL or MySQL)
- **Authentication**: JWT-based authentication
- **Testing**: Unittest with mocking (using `unittest.mock`)
- **API Documentation**: Automatically generated with Flask-RESTx Swagger UI
- **Containerization (Optional)**: Docker

## Setup Instructions

### Prerequisites
- **Python**: Version 3.9 or higher
- **Pip**: Python Package Manager
- **Virtual Environment**: Recommended (e.g., `venv` or similar)

### Steps to Set Up

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/siddiqua14/travel-api.git
   cd travel-api

   exit 

2. **Set Up Virtual Environment**:
     ```bash
     python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate