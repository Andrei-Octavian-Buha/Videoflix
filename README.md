# Videoflix

**Developer Akademie School Project**

A backend video streaming platform built with **Django REST Framework**. The application provides secure JWT authentication and automatically converts uploaded videos into multiple streaming resolutions (480p, 720p, and 1080p) using FFmpeg.

---

## Features

### Authentication

* Custom User model
* User registration
* User login
* JWT authentication
* Email verification
* Password reset via email
* Protected API endpoints
* Custom permissions

### Video Management

* Video upload through Django Admin
* Automatic video conversion after upload
* Multiple video resolutions generated automatically:

  * 480p
  * 720p
  * 1080p
* Stream videos according to the available resolutions
* Video metadata management

### Administration

* Django Admin Panel
* User management
* Video management
* Authentication management

---

## Technologies Used

### Backend

* Python
* Django
* Django REST Framework
* Simple JWT

### Database

* PostgreSQL

### Video Processing

* FFmpeg

### Containerization

* Docker
* Docker Compose

---

## Project Structure

```text
.
├── auth_app/              # Authentication application
├── video_app/             # Video management and streaming
├── core/                  # Django project configuration
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

## How the Application Works

### User Flow

1. A user creates an account.
2. The user verifies their email address.
3. The user logs into the application.
4. The server returns a JWT access token.
5. The authenticated user can access protected endpoints and watch available videos.

---

### Video Upload Flow

1. The administrator uploads a video through the Django Admin Panel.
2. The uploaded video is stored on the server.
3. FFmpeg automatically processes the original video.
4. Three additional versions of the video are generated:

   * 480p
   * 720p
   * 1080p
5. Users can stream the available resolutions.

---

# Installation

## Prerequisites

Before running the project, make sure you have installed:

* Docker
* Docker Compose
* Git

---

## Clone the Repository

```bash
git clone <repository-url>
cd Videoflix
```

---

## Environment Variables

Create a `.env` file from the provided template.

```bash
cp .env.template .env
```

Configure the required environment variables, for example:

```env
DEBUG=True

SECRET_KEY=your_secret_key

DB_NAME=videoflix
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123

REDIS_HOST=redis
REDIS_PORT=6379

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=True
```

---

## Run the Application

Build and start all containers.

```bash
docker compose up --build
```

The application starts three services:

* **PostgreSQL** – Database
* **Redis** – Background task queue
* **Django Backend** – REST API and video processing

---

## Automatic Startup Process

When the backend container starts, the entrypoint script automatically performs the following steps:

1. Waits until PostgreSQL is available.
2. Collects static files.
3. Creates and applies database migrations.
4. Creates a Django superuser (if one does not already exist).
5. Starts the Django RQ worker for background jobs.
6. Starts the Gunicorn application server.

No manual migration or superuser creation is required.

---

## Access the Application

Backend API:

```
http://localhost:8000/
```

Django Admin:

```
http://localhost:8000/admin/
```

Login using the superuser credentials defined in your `.env` file.

---

## Stopping the Application

```bash
docker compose down
```

To remove the containers and volumes:

```bash
docker compose down -v
```

---

## Useful Docker Commands

View running containers:

```bash
docker ps
```

View application logs:

```bash
docker compose logs -f
```

Restart the backend:

```bash
docker compose restart web
```

Rebuild after dependency changes:

```bash
docker compose up --build
```

---

## Video Processing

The Docker image includes **FFmpeg**, which is used to process uploaded videos.

Whenever an administrator uploads a video through the Django Admin Panel, the application automatically creates three optimized versions:

* 480p
* 720p
* 1080p

The conversion is handled as a background task using **Django RQ** and **Redis**, allowing users to continue using the application while the video is processed.


## Main Project Components

### auth_app

Responsible for:

* User authentication
* Registration
* Login
* JWT token management
* Email verification
* Password reset
* Custom user model

### video_app

Responsible for:

* Video upload
* Video storage
* Video processing
* Resolution conversion
* Video streaming

### core

Contains:

* Project settings
* URL routing
* Middleware
* Global configuration
* CORS configuration

---

## Future Improvements

* Adaptive streaming using HLS
* Video thumbnails
* Search videos
* Categories
* User watch history
* Favorites
* Video comments
* Unit and integration tests

---

## Author

**Andy**
