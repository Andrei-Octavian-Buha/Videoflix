# Authentication API

A Django REST Framework authentication backend that provides a complete user authentication system with JWT authentication, email verification, password reset functionality, and Docker support.

---

## Features

- Custom User model
- JWT Authentication
- User Registration
- User Login
- Email Verification
- Password Reset via Email
- Authentication Permissions
- Email Templates
- CORS Support for Frontend Development
- Docker & Docker Compose Support
- REST API built with Django REST Framework

---

## Tech Stack

- Python 3
- Django
- Django REST Framework
- Simple JWT
- PostgreSQL (recommended)
- Docker
- Docker Compose

---

## Project Structure

```text
.
├── auth_app/              # Authentication logic
├── core/                  # Project configuration
├── video_app/             # Video application (future module)
├── static/
│   └── images/
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── backend.Dockerfile
├── backend.entrypoint.sh
├── .env.template
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd authentication-api
```

---

## Environment Variables

Copy the template file.

```bash
cp .env.template .env
```

Update the environment variables according to your local setup.

Example:

```env
DEBUG=True

SECRET_KEY=your-secret-key

DB_NAME=database_name
DB_USER=database_user
DB_PASSWORD=database_password
DB_HOST=db
DB_PORT=5432

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=True
```

---

## Running without Docker

Create a virtual environment.

```bash
python -m venv venv
```

Activate it.

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```powershell
venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Apply migrations.

```bash
python manage.py migrate
```

Create a superuser.

```bash
python manage.py createsuperuser
```

Run the server.

```bash
python manage.py runserver
```

The API will be available at:

```
http://127.0.0.1:8000/
```

---

## Running with Docker

Build and start the containers.

```bash
docker compose up --build
```

Run migrations.

```bash
docker compose exec backend python manage.py migrate
```

Create a superuser.

```bash
docker compose exec backend python manage.py createsuperuser
```

The application will be available at:

```
http://localhost:8000/
```

---

## Authentication Flow

1. Register a new account.
2. Receive an email verification link.
3. Verify your email.
4. Login with your credentials.
5. Receive JWT Access and Refresh tokens.
6. Use the Access token to authenticate protected endpoints.
7. Refresh the Access token when it expires.

---

## Main API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login |
| POST | `/api/auth/logout/` | Logout |
| POST | `/api/auth/token/refresh/` | Refresh JWT token |
| POST | `/api/auth/password-reset/` | Request password reset |
| POST | `/api/auth/password-reset-confirm/` | Confirm password reset |
| GET | `/api/auth/verify-email/` | Verify email address |

> Adjust endpoint URLs if your project uses different routes.

---

## Development

Run migrations after model changes.

```bash
python manage.py makemigrations
python manage.py migrate
```

Collect static files.

```bash
python manage.py collectstatic
```

---

## Docker Commands

Start containers.

```bash
docker compose up
```

Start in detached mode.

```bash
docker compose up -d
```

Stop containers.

```bash
docker compose down
```

Rebuild containers.

```bash
docker compose up --build
```

View logs.

```bash
docker compose logs -f
```

---

## Project Modules

### auth_app

Contains:

- Custom User model
- Authentication
- Registration
- Login
- JWT
- Email verification
- Password reset
- Permissions
- User manager

### core

Contains:

- Django settings
- URL configuration
- Middleware
- CORS configuration
- Global project settings

### video_app

Module reserved for video-related functionality.

---

## Future Improvements

- OAuth (Google/GitHub)
- Two-Factor Authentication (2FA)
- User Profile API
- Rate Limiting
- Swagger / OpenAPI Documentation
- Unit & Integration Tests
- CI/CD Pipeline

---

## License

This project is licensed under the MIT License.

---

## Author

Developed by **Andy**.
