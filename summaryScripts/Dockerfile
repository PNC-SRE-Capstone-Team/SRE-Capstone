# Use the official Python image from Docker Hub
FROM python:3.12-slim

# Get Args
ARG MONGO_URI=${MONGO_URI}
ARG MYSQL_USER=${MYSQL_USER}
ARG MYSQL_PW=${MYSQL_PW}
ARG MYSQL_PORT=${MYSQL_PORT}

# Set ENV
ENV MONGO_URI=${MONGO_URI}
ENV MYSQL_USER=${MYSQL_USER}
ENV MYSQL_PW=${MYSQL_PW}
ENV MYSQL_PORT=${MYSQL_PORT}

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Set the default command to run the application
CMD ["python", "main.py"]
