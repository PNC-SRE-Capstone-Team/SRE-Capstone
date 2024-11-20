from confluent_kafka import Consumer
import joblib
import json
from pymongo import MongoClient

# Load the model
model = joblib.load('model.joblib')

# Kafka consumer setup
consumer = Consumer({
    'bootstrap.servers': 'kafka-controller-headless.kafka.svc.cluster.local:9092',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['transactions'])

# MongoDB connection, implement auth
client = MongoClient('mongodb://mongo:27017/')
db = client.prod
collection = db.logs

# Process Kafka messages
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue

    transaction = json.loads(msg.value().decode('utf-8'))
    features = preprocess_transaction(transaction)  # Implement this function
    prediction = model.predict([features])[0]
    transaction['Fraud'] = int(prediction)

    # Store in MongoDB
    collection.insert_one(transaction)

consumer.close()
