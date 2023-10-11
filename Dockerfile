# Use a base image with Python installed
FROM python:3.9-slim

# Set a working directory in the container
WORKDIR /app

# Copy the environment configuration file into the container
COPY .env .

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code and other necessary files into the container
COPY src/ .

# Specify the default command to run the script
ENTRYPOINT ["python"]

# Ensure the output directory is accessible from the host
VOLUME ["/app/output"]
