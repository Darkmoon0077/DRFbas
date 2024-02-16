#!/bin/bash
echo "Creating Migrations..."
python manage.py makemigrations
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================
echo "dumping data..."
python manage.py loaddata dump.json
echo ====================================

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000