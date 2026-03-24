# FastAPI Task Management API

A lightweight and feature-rich Task Management API built with FastAPI. It provides user authentication, task tracking, and the ability to generate PDF reports of your tasks. 

Currently, the application uses an in-memory data structure for storage, making it incredibly easy to set up and test.

## Features

- **User Authentication & Authorization**: Secure your API with JWT (JSON Web Tokens). Includes access and refresh tokens, secure password hashing using `bcrypt`, and cookie-based token management for enhanced security.
- **User Registration**: Create new user accounts easily.
- **Task Management**: Full CRUD operations for tasks. Users can create, view, update (mark as finished), and delete their tasks.
- **PDF Reports**: Automatically generate and download a PDF report containing a list of all your tasks and their current statuses.
- **Environment Configuration**: Easily configure settings using environment variables via `pydantic-settings`.

## Project Structure

The project follows a modular structure using FastAPI routers:

- `main.py`: The entry point for the FastAPI application. Registers all routers.
- `config.py`: Configuration file managing environment variables and application settings.
- `schemas.py`: Pydantic models for request and response validation.
- `storage.py`: In-memory storage components for users and tasks (acting as a mock database).
- `routers/`: Contains modular route definitions.
  - `auth.py`: Endpoints for login, token refresh, and logout.
  - `register.py`: Endpoints for checking and registering new users.
  - `tasks.py`: Endpoints for managing tasks (add, get, update, delete).
  - `raport.py`: Endpoints for generating PDF reports of user tasks.
- `utils/`: Reusable utility functions.
  - `auth_utils.py`: Authentication helpers like password hashing, token creation, and dependency injection to get the current user.
  - `storage_utils.py`: Helper functions to manage the in-memory database.

## Prerequisites

- Python 3.10+
- The following Python libraries: `fastapi`, `uvicorn`, `pydantic`, `pydantic-settings`, `PyJWT`, `bcrypt`, `fpdf`.


1. **Environment Variables**:
   Create a `.env` file in the root directory. You will need to define at minimum:
   ```env
   SECRET_KEY=your_super_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```

## Usage / Endpoints Summary

- **Authentication**
  - `POST /login`: Authenticate and receive access and refresh tokens.
  - `POST /refresh`: Refresh the access token using the stored cookie.
  - `POST /logout`: Clear session cookies.
- **Registration**
  - `POST /register/`: Create a new user account.
- **Tasks**
  - `POST /tasks/add`: Create a new task.
  - `GET /tasks`: Retrieve all tasks for the logged-in user.
  - `GET /tasks/{id}`: Retrieve a specific task by its ID.
  - `PATCH /tasks/update/mark_finished/{id}`: Mark a task as completed.
  - `DELETE /tasks/delete/{id}`: Delete a specific task.
- **Reports**
  - `GET /raport/generate`: Download a generated PDF file of all your tasks.

## Future Improvements

- Replace the in-memory `fake_users_db` and `tasks_list` with a persistent database (e.g., PostgreSQL or SQLite) 
