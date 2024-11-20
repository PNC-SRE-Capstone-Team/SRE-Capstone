from confluent_kafka import Consumer
import joblib
import json
from pymongo import MongoClient
import logging
import os

def main():
    #init mongo uri
    mongo_uri = os.getenv("MONGO_URI")

    # Load the model
    model = joblib.load('model.joblib')

    #Init logs
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info("Fraud Detection App Started Successfully!")

    # Kafka consumer setup
    consumer = Consumer({
    'bootstrap.servers': 'kafka-controller-headless.kafka.svc.cluster.local:9092',
    'group.id': 'fraud-detector',
    'auto.offset.reset': 'earliest'
    })



    # MongoDB connection
    client = MongoClient(mongo_uri)
    db = client.test
    collection = db.logs

    # Process Kafka messages
    while True:
        consumer.subscribe(['transactions'])
        logging.info("loop")
        msg = consumer.poll(1.0)
        logging.info(msg)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {logging.error(msg.error())}")
            continue

        logging.info()

        #Transform the incoming msg into a parsable json
        transaction = json.loads(msg.value().decode('utf-8'))
        logging.info(transaction)
        #features = preprocess_transaction(transaction)  # Implement this function
        #prediction = model.predict([features])[0]
        #transaction['Fraud'] = int(prediction)

        #logging.info(transaction)

        # Store in MongoDB
        #collection.insert_one(transaction)

        consumer.close()


if __name__ == "__main__":
    main()
