#!bin/bash

# Pull the latest images
@echo "Pulling the latest images"
docker compose pull

@echo "Shutting down containers if they are running"
docker compose down

@echo "Starting the containers"
docker compose up -d
