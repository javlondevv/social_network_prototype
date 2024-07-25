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

2. Create a `.env-compose` file with the following content:

    ```env
    POSTGRES_DB=yourdbname
    POSTGRES_USER=yourdbuser
    POSTGRES_PASSWORD=yourdbpassword
    MINIO_ROOT_USER=minioadmin
    MINIO_ROOT_PASSWORD=minioadmin
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
