FROM python:3.11.10-slim-bookworm

RUN pip install confluent-kafka==2.3.0

COPY kafkaSendLogs.py /
COPY CreditCardData.csv /

ENTRYPOINT ["/usr/local/bin/python3", "kafkaSendLogs.py"]
CMD ["CreditCardData.csv", "transactions"]
