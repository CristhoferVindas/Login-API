# User Management Project with Django and JWT

This project is a RESTful API built with Django and Django Rest Framework for user management, including features like registration, authentication, password change, user profile retrieval, and logout. It uses JWT (JSON Web Tokens) for secure authentication and supports the creation of access and refresh tokens.

## Features

- **User Registration**: Create a new user with password validation.
- **Authentication**: Obtain an access and refresh token using email and password.
- **Logout**: Invalidate a refresh token (logout).
- **User Profile**: Retrieve the profile information of the authenticated user.
- **Password Change**: Change the password of the authenticated user.

## Requirements

- Python 3.8 or higher
- Django 4.0 or higher
- Django Rest Framework 3.12 or higher
- djangorestframework-simplejwt 4.8 or higher

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/django-jwt-project.git
    cd django-jwt-project
    ```

2. **Install dependencies**:

    Make sure to set up a virtual environment (you can use `venv` or `virtualenv`).

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Configure the database**:

    If this is your first time setting up the project, run the migrations:

    ```bash
    python manage.py migrate
    ```

4. **Create a superuser** (optional to access Django admin):

    ```bash
    python manage.py createsuperuser
    ```

5. **Start the development server**:

    ```bash
    python manage.py runserver
    ```

    The server will be running at `http://127.0.0.1:8000/`.

## Endpoints

### 1. Create a New User
- **URL**: `/create-user/`
- **Method**: `POST`
- **Body** (JSON):
    ```json
    {
      "name": "User Name",
      "email": "email@example.com",
      "password": "secure_password"
    }
    ```
- **Response**:
    ```json
    {
      "message": "User created successfully!",
      "access": "access_token",
      "refresh": "refresh_token"
    }
    ```

### 2. Get Token (Login)
- **URL**: `/token/`
- **Method**: `POST`
- **Body** (JSON):
    ```json
    {
      "email": "email@example.com",
      "password": "secure_password"
    }
    ```
- **Response**:
    ```json
    {
      "access": "access_token",
      "refresh": "refresh_token"
    }
    ```

### 3. Logout
- **URL**: `/logout/`
- **Method**: `POST`
- **Body** (JSON):
    ```json
    {
      "refresh": "refresh_token"
    }
    ```
- **Response**:
    ```json
    {
      "message": "Logged out successfully"
    }
    ```

### 4. Get User Profile
- **URL**: `/profile/`
- **Method**: `GET`
- **Response**:
    ```json
    {
      "name": "User Name",
      "email": "email@example.com",
      "creation_date": "2025-04-25T00:00:00Z"
    }
    ```

### 5. Change Password
- **URL**: `/change-password/`
- **Method**: `POST`
- **Body** (JSON):
    ```json
    {
      "old_password": "old_password",
      "new_password": "new_password"
    }
    ```
- **Response**:
    ```json
    {
      "message": "Password changed successfully"
    }
    ```

### 6. Refresh Token
- **URL**: `/refresh/`
- **Method**: `POST`
- **Body** (JSON):
    ```json
    {
      "refresh": "refresh_token"
    }
    ```
- **Response**:
    ```json
    {
      "access": "new_access_token"
    }
    ```

## Error Handling

- **404 Not Found**: If an endpoint is not found.
    ```json
    {
      "error": "The endpoint was not found"
    }
    ```

- **500 Internal Server Error**: If an internal server error occurs.
    ```json
    {
      "error": "Internal server error"
    }
    ```

## Security

- **JWT**: Authentication is handled using JWT tokens, ensuring secure communication with the server.
- **Passwords**: Passwords are validated and stored securely using Django's `set_password` function.

## Contributing

Contributions are welcome! If you'd like to improve this project, please fork it and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

