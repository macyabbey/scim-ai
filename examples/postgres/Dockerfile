# syntax=docker/dockerfile:1

FROM postgres:15-alpine

# Copy ecommerce initialization scripts
COPY ./vanilla-ecommerce/schema/init-db.sql /docker-entrypoint-initdb.d/01-init-db.sql
COPY ./vanilla-ecommerce/schema/init-schema.sql /docker-entrypoint-initdb.d/02-init-schema.sql
COPY ./vanilla-ecommerce/schema/init-seed-data.sql /docker-entrypoint-initdb.d/03-init-seed-data.sql

# Copy pheonix db initialization scripts
COPY ./pheonix/schema/init-db.sql /docker-entrypoint-initdb.d/04-init-pheonix-db.sql


# Expose the PostgreSQL port
EXPOSE 5432