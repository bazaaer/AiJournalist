@echo off

REM Check if the .env file exists
IF NOT EXIST ".env" (
    echo Error: .env file not found. Please create a .env file before running this script.
    PAUSE
    EXIT /B 1
)

REM Pull the latest images
echo Pulling the latest images
docker compose pull

REM Shut down containers if they are running
echo Shutting down containers if they are running
docker compose down

REM Start the containers (without -d to keep the window open)
echo Starting the containers
docker compose up -d

REM Keep the window open
echo.
pause
