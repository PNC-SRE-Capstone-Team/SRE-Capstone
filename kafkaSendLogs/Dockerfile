FROM python:3.11.10-slim-bookworm

COPY requirements.txt .
COPY kafkaSendLogs.py .
COPY CreditCardData.csv .

RUN pip install -r requirements.txt

ENTRYPOINT ["/usr/local/bin/python3", "kafkaSendLogs.py"]
CMD ["CreditCardData.csv", "transactions"]
