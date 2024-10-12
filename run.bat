# Pull the latest images
Write-Output "Pulling the latest images"
docker compose pull

# Shutting down containers if they are running
Write-Output "Shutting down containers if they are running"
docker compose down

# Starting the containers
Write-Output "Starting the containers"
docker compose up -d