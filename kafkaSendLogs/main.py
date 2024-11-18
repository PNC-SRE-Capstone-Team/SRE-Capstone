#!/usr/bin/env python3

"""Generates a stream to Kafka from a time series CSV file.
"""

import argparse
import csv
import datetime
import json
import socket
import sys
import time

from confluent_kafka import Producer


# Send ~100 transactions per second.
# Runtime of 16m40s for 100,000 transactions.
TRANSACTION_INTERVAL = 0.01


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg.value()), str(err)))
    else:
        print("Message produced: %s" % (str(msg.value())))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filename', type=str, help='Credit card CSV file.')
    parser.add_argument('topic', type=str, help='Name of the Kafka topic to stream.')
    parser.add_argument('--speed', type=float, default=1, required=False,
                        help='Speed up time series by a given multiplicative factor.')

    args = parser.parse_args()

    topic = args.topic
    fname = args.filename
    speed = args.speed

    conf = {'bootstrap.servers': 'localhost:9092',
            'client.id': socket.gethostname()}
    producer = Producer(conf)

    with open(fname, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = {
                # CSV starts with an invisible unicode char.
                "transaction_id": row['\ufeffTransaction ID'],
                "date": row['Date'],
                "day_of_week": row['Day of Week'],
                "time": row['Time'],
                "card_type": row['Type of Card'],
                "entry_mode": row['Entry Mode'],
                "amount": row['Amount'],
                "transaction_type": row['Type of Transaction'],
                "merchant_group": row['Merchant Group'],
                "transaction_country": row['Country of Transaction'],
                "shipping_address": row['Shipping Address'],
                "residence_country": row['Country of Residence'],
                "gender": row['Gender'],
                "age": row['Age'],
                "bank": row['Bank'],
                "fraud": row['Fraud'],
            }

            try:
                producer.produce(topic, key=data["transaction_id"],
                                 value=json.dumps(data).encode('utf-8'),
                                 callback=acked)
            except TypeError:
                sys.exit(1)

            producer.flush()

            time.sleep(TRANSACTION_INTERVAL * speed)


if __name__ == "__main__":
    main()
