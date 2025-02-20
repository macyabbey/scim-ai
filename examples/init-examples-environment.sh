#!/bin/bash
docker container stop examples-pgadmin-1
docker container stop examples-postgres-db-1
docker container rm examples-pgadmin-1
docker container rm examples-postgres-db-1
docker volume rm examples_db_data
docker-compose up -d --build