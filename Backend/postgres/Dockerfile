FROM postgres:15.2-alpine

ENV POSTGRES_DB pip

COPY ./test_data/* /docker-entrypoint-initdb.d/
COPY ./schema/* /docker-entrypoint-initdb.d/

# Ensure schema.sql gets run first by making it first alphabetically
RUN mv /docker-entrypoint-initdb.d/schema.sql /docker-entrypoint-initdb.d/aaaaa.sql