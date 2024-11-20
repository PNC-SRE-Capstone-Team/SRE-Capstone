from confluent_kafka import Consumer
import joblib
import json
from pymongo import MongoClient
import logging
import os
from datetime import datetime
import pandas as pd

# Load the model
model = joblib.load('model.joblib')

# Load trained feature names
trained_columns = joblib.load('trained_columns.joblib')  

def preprocess_transaction(data):
    # Filter out unneeded keys
    filtered_data = {key: value for key, value in data.items() if key not in ['transaction_id', 'date', 'fraud']}

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
    formatted_data = {key_format_mapping[key]: value for key, value in filtered_data.items()}
    
    # Convert the transaction dictionary to a DataFrame
    df = pd.DataFrame([formatted_data])

        # Convert numeric fields
    numeric_fields = ['Amount', 'Age', 'Time']  # Specify fields that should be numeric
    for field in numeric_fields:
        if field in df:
            df[field] = (
                df[field].str.replace('£', '').astype(float) if df[field].dtype == object else df[field]
            )

    # One-hot encode categorical columns
    df = pd.get_dummies(df)

    # Align with training columns (fill missing columns with 0)
    df = df.reindex(columns=trained_columns, fill_value=0)

    # Convert the processed row back to a dictionary
    processed_data = df.iloc[0]

    logging.info("processed data:" + processed_data)  # Return as a NumPy array (1D)

    return processed_data # Return as a NumPy array (1D)



def main():


    #init mongo uri
    mongo_uri = os.getenv("MONGO_URI")

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
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {logging.error(msg.error())}")
            continue

        #Transform the incoming msg into a parsable json
        transaction = json.loads(msg.value().decode('utf-8'))
        logging.info(transaction)
        
        #transactionDict = json.loads(transaction)
        #process and predict fraud
        features = preprocess_transaction(transaction)
        try:
            prediction = model.predict([features])[0]
        except:
            logging.warning("prediction failure")

        features['Fraud'] = int(prediction)
        features['ID'] = transaction['transaction_id']

        # Get the current UTC datetime
        current_datetime = datetime.utcnow()
        
        features['Date'] = current_datetime.strftime("%Y-%m-%d")
        features['Time'] = current_datetime.strftime("%H:%M:%S.%f")

        # Store in MongoDB
        collection.insert_one(features)

        logging.info("Inserted document: " + features)



    consumer.close()


if __name__ == "__main__":
    main()
