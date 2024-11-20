from confluent_kafka import Consumer
import joblib
import json
from pymongo import MongoClient
import logging
import os
from datetime import datetime
import pandas as pd

#Prometheus libraries
from prometheus_client import Counter, Gauge, start_http_server

# Create Prometheus metrics
transaction_counter = Counter(
    'transactions_total', 'Total number of transactions', ['transaction_type', 'country']
)
fraud_counter = Counter(
    'fraudulent_transactions_total', 'Total number of fraudulent transactions', ['country']
)
transaction_amount = Gauge(
    'transaction_amount', 'Amount of the last transaction', ['transaction_type', 'country']
)


# Load the model
model = joblib.load('model.joblib')

# Load trained feature names
trained_columns = joblib.load('trained_columns.joblib')


def process_transaction(transaction):
    """
    Process a transaction and update Prometheus metrics.
    """
    try:
        transaction_type = transaction.get('Type of Transaction', 'unknown')
        country = transaction.get('Country of Transaction', 'unknown')
        amount_str = str(transaction.get('Amount', 0))
        amount = float(amount_str.replace('£', '').replace('€', '').strip())
        is_fraud = transaction.get('Fraud', 0)

        # Increment transaction counter
        transaction_counter.labels(transaction_type=transaction_type, country=country).inc()

        # Update the transaction amount gauge
        transaction_amount.labels(transaction_type=transaction_type, country=country).set(amount)

        # Increment fraud counter if the transaction is fraudulent
        if is_fraud == 1:
            fraud_counter.labels(country=country).inc()

    except:
        logging.info("Processing error for prometheus")



def preprocess_transaction(data):

    
    # Convert the transaction dictionary to a DataFrame
    df = pd.DataFrame([data])

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

    return processed_data # Return as a NumPy array (1D)



def main():
    start_http_server(8000, addr="0.0.0.0")  # Exposes metrics on http://localhost:8000/metrics

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
    db = client.prod
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
        #logging.info(transaction)

        if transaction['amount'] == '':
            transaction['amount'] = '£1'

            # Filter out unneeded keys
        filtered_data = {key: value for key, value in transaction.items() if key not in ['transaction_id', 'date', 'fraud']}

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

        try:
            # Apply the new key format
            formatted_data = {key_format_mapping[key]: value for key, value in filtered_data.items()}
        except:
            logging.warning("Couldn't format data")
            continue
        
        #transactionDict = json.loads(transaction)
        #process and predict fraud
        features = preprocess_transaction(formatted_data)
        try:
            prediction = model.predict([features])[0]
        except:
            logging.warning("prediction failure")
            prediction = 0

        formatted_data['Fraud'] = int(prediction)
        formatted_data['ID'] = transaction['transaction_id']

        # Get the current UTC datetime
        current_datetime = datetime.now(datetime.timezone.utc)
        
        formatted_data['Date'] = current_datetime.strftime("%Y-%m-%d")
        formatted_data['Time'] = current_datetime.strftime("%H:%M:%S.%f")

        process_transaction(formatted_data)

        # Store in MongoDB
        collection.insert_one(formatted_data)

        #logging.info("Inserted document: " + str(formatted_data))



    consumer.close()


if __name__ == "__main__":
    main()
