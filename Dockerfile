# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim-buster AS base

# EXPOSE 8000

# ENV PORT=8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# add pipenv venv folder in the same dir
ENV PIPENV_VENV_IN_PROJECT=1

# Install pip requirements
RUN python -m pip install --upgrade pip \
    && apt-get update && apt-get install -y libpq-dev python-dev gcc \
    && pip install --no-cache-dir pipenv

# RUN pip install virtualenv
# RUN virtualenv venv

WORKDIR /app
# COPY . .
COPY ./project4 ./project4
COPY ./network ./network
COPY ./manage.py ./
COPY ./entrypoint_prod* ./
COPY ./Pipfile ./
# COPY ./Pipfile.lock ./
COPY ./requirements.txt ./


# RUN pipenv lock
RUN pipenv install \
    # Creates a non-root user with an explicit UID and adds permission to access the /app folder
    # For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
    && adduser -u 5678 --disabled-password --gecos "" appuser \
    && mkdir -p /app/static && mkdir -p /app/media \
    && chown -R appuser /app
    # && chmod -R 755 /app

USER appuser

# ENTRYPOINT [ "./entrypoint_prod.sh" ]
CMD pipenv run python manage.py makemigrations --no-input \
    && pipenv run python manage.py migrate --no-input \
    && pipenv run python manage.py collectstatic --no-input --ignore frontend \
    && pipenv run gunicorn project4.wsgi:application --bind 0.0.0.0:$PORT

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found in subfolder: 'network'. Please enter the Python path to wsgi file.
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pythonPath.to.wsgi"]