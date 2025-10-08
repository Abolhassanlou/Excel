# Mamafood

## Todos

- [ ] Ordnerstruktur
- [ ] Besprechungstermin

## Ordnerstruktur

- /doc
- /thesis
- /src
- /org/meetings/YYYY-MM-DD.md
- /org/issues.yaml
- /org/worklog.csv
figma link für Design:
https://www.figma.com/design/nQLJGEJUgw1CaAUhn55US1/Profile?m=auto&t=y08OHUioyFNlz9qp-1

## Running Docker
FastAPI Authentication APIs - Test Driven Development (TDD)

This project provides a set of FastAPI authentication APIs, developed using a Test-Driven Development (TDD) approach, and designed to run seamlessly with Docker.

Table of Contents

    APIs

    Prerequisites

    Installation & Configuration

    Building & Running the Project

    Accessing Services

    Database Migrations

    Running Tests

APIs

(Optional: Add a brief description of what these APIs do, e.g., "This project includes APIs for user registration, login, profile management, and more, serving as the authentication backend for the MamaFood platform.")

Prerequisites

Before you begin, ensure you have the following installed:

    Docker Desktop: This includes Docker Engine and Docker Compose.

        Download Docker Desktop

Installation & Configuration

    Start Docker Desktop: Ensure Docker Desktop is running on your machine.

    Clone the Repository:
    Bash

git clone [https://github.com/Abolhassanlou/Mamafood.git]


Navigate to Project Directory:
Bash

cd mamafood/backend/fastapi-mamafood

Create Docker Volume: This volume is essential for persisting your MySQL data across container restarts.
Bash

    docker volume create mamafood_mysql_data

    Database Connection Details:
    Your docker-compose.yml and services are pre-configured with the following MySQL connection details:

    MYSQL_HOST=mysql
    MYSQL_USER=root
    MYSQL_PASSWORD=mamafood
    MYSQL_DB=mamafood
    MYSQL_PORT=3306
.

Building & Running the Project

    Build Docker Images: This command builds the necessary Docker images for all services defined in docker-compose.yml.
    Bash

docker-compose build

Start Services: Once the build is complete, start all services in detached mode (recommended for a clean terminal) or in the foreground.

Bash

docker-compose up

(Leave this terminal open to monitor service logs. Press Ctrl + C to stop services.)

Detached Mode (recommended):
Bash

        docker-compose up -d

Ctrl + c (To stop services in detached mode, run docker-compose down.)

Accessing Services

Once services are up and running, you can access them via your web browser:

    FastAPI Application Status: http://localhost:8000

    FastAPI API Documentation (Swagger UI): http://localhost:8000/docs

    phpMyAdmin (Database Access): http://localhost:8080

    Use the MySQL connection details mentioned above (MYSQL_USER=root, MYSQL_PASSWORD=mamafood, MYSQL_DB=mamafood) to log in.

    Mailpit (Email Testing): http://localhost:8025

    (This is useful for catching emails sent by the application, such as registration verification or password reset links.)

Database Migrations

This project uses Alembic for database migrations.

Generate New Migration from Model Changes:
Bash

docker-compose run fastapi-service /bin/sh -c "alembic revision --autogenerate -m 'your_migration_message'"

(Replace 'your_migration_message' with a descriptive message for your changes, e.g., 'create initial tables' or 'add user email field'.)

Apply Pending Migrations to Database (Upgrade):
Bash

docker-compose run fastapi-service /bin/sh -c "alembic upgrade head"

Revert Last Applied Migration (Downgrade):
Bash

docker-compose run fastapi-service /bin/sh -c "alembic downgrade -1"

Running Tests

Tests are managed with Pytest.

Run All Tests:
Bash

docker-compose run fastapi-service /bin/sh -c "pytest"

Display Info Logs During Tests:
Bash

docker-compose run fastapi-service /bin/sh -c "pytest --log-cli-level=INFO"

Run a Single Test File:
Bash

docker-compose run fastapi-service /bin/sh -c "pytest tests/test_user_routes/test_user_regis
