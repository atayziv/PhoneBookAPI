FROM python:3.9-slim
USER root
WORKDIR /usr/src/app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry==1.4.2

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --without-urls

RUN pip install -r requirements.txt

COPY main.py ./
COPY phone_book_api_server phone_book_api_server

ENV LISTEN_PORT=8000
EXPOSE 8000

# Define the command to run the application
CMD ["python","main.py"]
