#!/bin/sh

echo "Waiting for MinIO to be ready..."
while ! curl -s http://minio:9000/minio/health/live; do
    sleep 1
done

echo "Configuring MinIO Client..."
mc alias set myminio http://minio:9000 minioadmin minioadmin
mc admin config set myminio/ --json /usr/src/app/cors-config.json

echo "Running Django migrations..."
python manage.py migrate
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8001
