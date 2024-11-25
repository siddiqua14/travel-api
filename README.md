# Travel API with Microservices

This project implements a Travel API using a microservices architecture, ensuring scalability and separation of concerns. It provides services for managing users, destinations, and authentication.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Technologies Used](#technologies-used)
3. [Setup Instructions](#setup-instructions)
   - [Prerequisites](#prerequisites)
   - [Steps to Set Up](#steps-to-set-up)
4. [API Endpoints](#api-endpoints)
   - [User Service](#1-user-service)
   - [Authentication Service](#2-authentication-service)
   - [Destination Service](#3-destination-service)
5. [Testing](#testing)
6. [Example Workflow](#example-workflow)

## Project Structure

1. **User Management**:  
   - Register new users.
   - Login
   - View profile  
   - Manage user roles (admin and regular users).  

2. **Secure Authentication**:  
   - JWT-based authentication for secure access.  
   - Role-based access control (e.g., admin-only actions).  

3. **Destination Management**:  
   - View all destinations.  
   - Add or delete destinations (admin-only access).  


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
     python3 -m venv .venv    # On Windows:py -3 -m venv .venv
     source .venv/bin/activate  # On Windows: .venv\Scripts\activate
     pip install Flask   # Install Flask

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
    `pytest tests/`
    
-Test output will display test coverage and results:
   `pytest --cov=app tests/`
    
## Example Workflow

1. **Register a User**:  
   Send a request to `/users/register` to create a new user.

2. **Login**:  
   Authenticate via `/auth/login` to obtain a JWT token.

3. **Authenticated Requests**:  
   Use the token to make authenticated requests, such as adding or deleting destinations.
