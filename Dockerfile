#ARG ARTIFACTORY_PROXY="jf.originai.co"
#ARG ECO_ARTIFACTORY_PROXY="jf.originai.co/docker"
#
## --------------> The build image
#FROM python:3.9-slim
#ARG DATABASE_URL
#ENV DATABASE_URL=$DATABASE_URL
#ARG ARTIFACTORY_PROXY
#ARG ARTI_USERNAME
#ARG ARTI_PASSWORD
#ARG ARTI_PROTOCOL="https"
#ARG ARTI_PYPI_REPO="${ARTIFACTORY_PROXY}/artifactory/api/pypi/pypi/simple"
#
#ENV ARTI_USER_PASS=${ARTI_USERNAME:+"${ARTI_USERNAME}:${ARTI_PASSWORD}@"}
#ENV ARTI_PYPI_URL="${ARTI_PROTOCOL}://${ARTI_USER_PASS}${ARTI_PYPI_REPO}"
#
## Set environment variables
#ENV PYTHONUNBUFFERED 1
#
## Install system dependencies
#RUN apt-get update \
#    && apt-get install -y gcc libpq-dev \
#    && rm -rf /var/lib/apt/lists/*
#
#USER root
#WORKDIR /usr/src/app
#
#COPY pyproject.toml poetry.lock ./
#
#RUN pip install --no-cache-dir poetry==1.4.2
#
#RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --without-urls
#
#RUN pip install -r requirements.txt
#
#COPY main.py ./
#COPY phone_book_api_server phone_book_api_server
#
## Create the .env file
##RUN touch phone_book_api_server/.env
#RUN echo "DATABASE_URL=${DATABASE_URL}" > phone_book_api_server/.env
#
#ENV LISTEN_PORT=8000
#EXPOSE 8000
#
## Define the command to run the application
#CMD ["python","main.py"]
