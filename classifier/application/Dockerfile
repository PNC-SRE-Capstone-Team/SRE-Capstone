FROM python:3.12-slim

# Get Args
ARG MONGO_URI=${MONGO_URI}

# Set ENV
ENV MONGO_URI=${MONGO_URI}

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Set the default command to run the application
CMD ["python", "detectionApplication.py"]
