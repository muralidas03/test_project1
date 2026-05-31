#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Wait for database if needed (when using MySQL/Postgres in Docker Compose)
if [ "$DB_HOST" != "" ] && [ "$DB_HOST" != "localhost" ]; then
    echo "Waiting for database at $DB_HOST:$DB_PORT..."
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done
    echo "Database is ready."
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Initialize default roles and permissions
echo "Initializing roles and permissions..."
python manage.py init_roles

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start server
echo "Starting server..."
# Using runserver for development, gunicorn would be better for production
# But since the project defaults to development settings, we use runserver
exec python manage.py runserver 0.0.0.0:8000
