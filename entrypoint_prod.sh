#!/bin/sh

set -e

pipenv run python manage.py makemigrations --no-input
pipenv run python manage.py migrate --no-input
pipenv run python manage.py collectstatic --no-input --ignore frontend

pipenv run gunicorn project4.wsgi:application --bind 0.0.0.0:$PORT