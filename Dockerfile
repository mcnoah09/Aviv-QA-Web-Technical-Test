FROM ubuntu:latest

# Set noninteractive mode
ENV DEBIAN_FRONTEND=noninteractive

# Install python3.10 and pip3
RUN apt-get update && apt-get install -y python3.10 python3-pip

WORKDIR /aviv-web-technical-test

RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install --no-cache-dir poetry==1.7.1

# Install chrome browser
RUN apt-get update && apt-get install -y wget gnupg2
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get install -y google-chrome-stable

ENV POETRY_VIRTUALENVS_CREATE=false

COPY poetry.lock pyproject.toml README.md ./
COPY tests ./tests

EXPOSE 80

RUN python3 -m poetry install --all-extras --verbose
