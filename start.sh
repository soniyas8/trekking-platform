#!/bin/bash
echo "Running migrations..."
python manage.py migrate --noinput
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "Starting gunicorn..."
gunicorn trekking_agency.wsgi --log-file -