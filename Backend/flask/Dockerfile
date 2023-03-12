# An image to work off of, instead of from scratch
# FROM python:3.9-alpine
FROM python:3.8-slim

# Copy over (and install) all requirements
RUN mkdir /src
COPY ./requirements.txt /src
RUN pip install -r /src/requirements.txt

# Copy over rest of source files
COPY ./src /src