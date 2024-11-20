FROM python:3.11.10-slim-bookworm

# Set the working directory inside the container
WORKDIR /app

# Copy the application code into the container
COPY kafkaSendLogs.py .
COPY requirements.txt .
COPY CreditCardData.csv .

# Install Python dependencies
RUN pip install -r requirements.txt

ENTRYPOINT ["/usr/local/bin/python3", "kafkaSendLogs.py"]
CMD ["CreditCardData.csv", "transactions"]
