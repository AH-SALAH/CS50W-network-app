#!/bin/sh

set -e

# whoami && which python && echo $PATH && ls -l `which sh` && echo $PYTHONPATH 
# ls -a ./ && pwd
# ls -a ./.venv/bin
# python -m site --user-base
# . .venv/bin/activate

pipenv run python manage.py runserver 0.0.0.0:$PORT
