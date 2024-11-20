from confluent_kafka import Consumer
import joblib
import json
from pymongo import MongoClient
import logging
import os
from datetime import datetime

def preprocess_transaction(data):
    # Filter out unneeded keys
    filtered_data = {key: value for key, value in formatted_data.items() if key not in ['transaction_id', 'date', 'fraud']}
    return filtered_data



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

    logging.info(consumer)

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

        #Transform the incoming msg into a parsable json
        transaction = json.loads(msg.value().decode('utf-8'))
        logging.info(transaction)

        #process and predict fraud
        features = preprocess_transaction(transaction)
        prediction = model.predict([features])[0]

        # Map old keys to new formatted keys
        key_format_mapping = {
        'day_of_week': 'Day of Week',
        'time': 'Time',
        'card_type': 'Type of Card',
        'entry_mode': 'Entry Mode',
        'amount': 'Amount',
        'transaction_type': 'Type of Transaction',
        'merchant_group': 'Merchant Group',
        'transaction_country': 'Country of Transaction',
        'shipping_address': 'Shipping Address',
        'residence_country': 'Country of Residence',
        'gender': 'Gender',
        'age': 'Age',
        'bank': 'Bank'
        }

        # Apply the new key format
        formatted_data = {key_format_mapping[key]: value for key, value in features.items()}


        features['Fraud'] = int(prediction)
        features['ID'] = transaction['transaction_id']

        # Get the current UTC datetime
        current_datetime = datetime.utcnow()
        
        features['Date'] = current_datetime.strftime("%Y-%m-%d")
        features['Time'] = current_datetime.strftime("%H:%M:%S.%f")

        logging.info(features)

        # Store in MongoDB
        collection.insert_one(features)



    consumer.close()


if __name__ == "__main__":
    main()
