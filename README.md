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

Before running the project, make sure the following software is installed on your machine:

- Git
- Docker
- Docker Compose

> **Note:** Python, Django, PostgreSQL, Redis, FFmpeg, and all project dependencies are installed automatically inside the Docker containers. No local Python environment is required.

---

## 1. Clone the Repository

```bash
git clone <repository-url>
cd Videoflix
```

---

## 2. Create the Environment File

Create a `.env` file from the provided template.

```bash
cp .env.template .env
```

The template contains default values for local development, including a development `SECRET_KEY`.

---

## 3. Build and Start the Application

Build the Docker image and start all required services.

```bash
docker compose up --build
```

During startup, the backend automatically:

- Waits for the PostgreSQL database to become available.
- Collects static files.
- Creates and applies database migrations.
- Creates a Django superuser (if one does not already exist).
- Starts the Django RQ worker.
- Launches the Gunicorn application server.

The following services will be running:

- **PostgreSQL** – Database
- **Redis** – Background task queue
- **Django Backend** – REST API and video processing

---

## 4. (Optional) Generate a New Django Secret Key

The `.env.template` file contains a development `SECRET_KEY`. For better security, you can generate your own unique key after the containers are running.

Run the following command:

```bash
docker compose exec web python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated key and replace the `SECRET_KEY` value in your `.env` file.

Example:

```env
SECRET_KEY=your_generated_secret_key
```

---

## 5. Restart the Application

Restart the containers to apply the new `SECRET_KEY`.

```bash
docker compose down
docker compose up
```

---

## Access the Application

Once the containers are running, the application will be available at:

### Backend API

```
http://localhost:8000/
```

### Django Admin

```
http://localhost:8000/admin/
```

Log in using the superuser credentials defined in your `.env` file.

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
