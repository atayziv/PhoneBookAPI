# --------------> The build image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

USER root
WORKDIR /app
WORKDIR /app/phone_book_api_server

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry==1.4.2

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --without-urls

RUN pip install -r requirements.txt

RUN poetry config certificates.arti.cert false

COPY main.py ./
COPY phone_book_api_server phone_book_api_server

ENV LISTEN_PORT=8000
EXPOSE 8000
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Define the command to run the application
CMD ["python","main.py"]
