# Social Network Prototype

A social network prototype built using Django that allows users to register, login, create posts, like posts, and update their profiles. The project includes Docker support for containerized deployment with PostgreSQL and Minio for file storage.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Forms](#forms)
- [Models](#models)
- [Docker Configuration](#docker-configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and authentication
- Profile management
- Post creation and listing
- Liking posts
- Notifications for likes
- Dockerized deployment with PostgreSQL and Minio

## Technologies

- Django
- PostgreSQL
- Minio
- Docker

## Setup

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/javlondevv/social-network-prototype
    cd social-network-prototype
    ```


# 2. Environment Configuration

This document provides the configuration settings for the `.env-compose` file required for your Django project. 

## `.env-compose` Configuration

Create a file named `.env-compose` in your project directory and add the following content:

```env
SECRET_KEY=django-insecure-^xn9cj!e+)q_t8b-ttbe8cka=1s#s==%#m5(l(xsqt($f*!ag!
DEBUG=True
ALLOWED_HOSTS=*
DB_NAME=social_db
DB_USER=social_user
DB_PASS=pL2aM2tS1kpL
DB_PORT=5432
DB_HOST=postgres
POSTGRES_USER=social_user
POSTGRES_DB=social_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_PASSWORD=pL2aM2tS1kpL
DB_ENGINE=django.db.backends.postgresql_psycopg2
MINIO_ENDPOINT=minio:9000
EXTERNAL_MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=mybucket
MINIO_CONSISTENCY_CHECK_ON_START=True
DEFAULT_FILE_STORAGE=storages.backends.s3boto3.S3Boto3Storage
AWS_S3_FILE_OVERWRITE=False
```

3. Build and start the containers:

    ```bash
    docker-compose up --build
    ```

4. Apply migrations and create a superuser:

    ```bash
    docker-compose exec web_service python manage.py migrate
    docker-compose exec web_service python manage.py createsuperuser
    ```

5. Access the application at `http://localhost:8005`.

## Usage

### Creating a New User

1. Go to `http://localhost:8005/profile/` to register a new user.
2. Fill in the registration form and submit.

### Logging In

1. Go to `http://localhost:8005/login/` to log in with your credentials.

### Creating a Post

1. Go to `http://localhost:8005/posts/create/` to create a new post.
2. Fill in the form with the title and content of your post and submit.

### Liking a Post

1. View posts at `http://localhost:8005/posts/`.
2. Click the like button on any post to like it.

### Updating Profile

1. Go to `http://localhost:8005/profile-update/` to update your profile information.
2. Fill in the form and submit.

## Project Structure

```plaintext
social-network-prototype/
├── apps/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
├── media/
├── static/
├── templates/
│   ├── registration/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── post_detail.html
│   ├── post_form.html
│   ├── profile.html
│   ├── register.html
├── Dockerfile
├── docker-compose.yaml
├── manage.py
└── requirements.txt
