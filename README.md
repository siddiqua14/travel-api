# Travel API with Microservices

This project implements a Travel API using a microservices architecture, ensuring scalability and separation of concerns. It provides services for managing users, destinations, and authentication.

## Project Structure

- **User Service**: Manages user data, including registration, authentication, and role management.
- **Destination Service**: View destinations. Post and Delete a specific travel destination (Admin-only).
- **Authentication Service**: Provides JWT-based authentication and role-based access control.

## Technologies Used

- **Backend**: Flask, Flask-RESTx
- **Authentication**: JWT-based authentication
- **Testing**: Unittest with mocking (using `unittest.mock`)
- **API Documentation**: Automatically generated with Flask-RESTx Swagger UI
- **Containerization (Optional)**: Docker

## Setup Instructions

### Prerequisites
- **Python**: Version 3.9 or higher
- **Pip**: Python Package Manager
- **Virtual Environment**: Recommended (e.g., `venv` )

### Steps to Set Up

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/siddiqua14/travel-api.git
   cd travel-api

   

2. **Set Up Virtual Environment**:
     ```bash
     python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
    
3. **Install Dependencies**:
     ```bash
    pip install -r requirements.txt
    flask run
    
4. **Run the Services**
   Navigate to each service folder:
   - `user-service`
   - `destination-service`
   - `authentication-service`
   Start each service using : 
   ```bash 
   python run.py
   

5. **API Endpoints**

    #### 1. User Service
    - **Base URL**: `http://localhost:5000`

    #### 2. Authentication Service
    - **Base URL**: `http://localhost:5001`

    #### 3. Destination Service
    - **Base URL**: `http://localhost:5002`

6. **Testing**

-To run tests for all services:
    ```bash
    pytest tests/
    
-Test output will display test coverage and results:
    ```bash
    pytest --cov=app tests/
    

## Example Workflow

1. **Register a User**:  
   Send a request to `/users/register` to create a new user.

2. **Login**:  
   Authenticate via `/auth/login` to obtain a JWT token.

3. **Authenticated Requests**:  
   Use the token to make authenticated requests, such as adding or deleting destinations.
