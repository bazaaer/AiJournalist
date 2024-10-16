#!/bin/bash

# Check if the .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found. Please create a .env file before running this script."
    exit 1
fi

# Pull the latest images
echo "Pulling the latest images"
docker compose pull

# Shut down containers if they are running
echo "Shutting down containers if they are running"
docker compose down

# Start the containers (without -d to keep the window open)
echo "Starting the containers"
docker compose up -d

# Keep the window open
read -p "Press any key to exit..."
