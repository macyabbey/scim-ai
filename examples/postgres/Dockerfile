# syntax=docker/dockerfile:1

FROM postgres:15-alpine

# Copy initialization scripts
COPY ./vanilla-ecommerce/schema/init-db.sql /docker-entrypoint-initdb.d/01-init-db.sql
COPY ./vanilla-ecommerce/schema/init-schema.sql /docker-entrypoint-initdb.d/02-init-schema.sql
COPY ./vanilla-ecommerce/schema/init-seed-data.sql /docker-entrypoint-initdb.d/03-init-seed-data.sql

# Expose the PostgreSQL port
EXPOSE 5432