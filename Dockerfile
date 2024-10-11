# Use the official Python base image
FROM python:3.12-bullseye

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY main.py api.py upload.py websearch.py ./

# Set the entrypoint command to run the backend, passing in the environment variables
CMD ["sh", "-c", "python main.py $COUNT $IMG_OPTION"]
