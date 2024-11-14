from faker import Faker
import pandas as pd
import random
import time
import os

# Initialize Faker
fake = Faker()

# Set the number of initial records and records per interval
initial_records = 100
interval_records = 10

# Define the CSV file name
csv_file = "FakeCreditCardDataNew.csv"

# Function to generate data
def generate_data(num_records):
    data = {
        "Transaction ID": [f"#{random.randint(1000, 9999)} {random.randint(100, 999)}" for _ in range(num_records)],
        "Date": [fake.date_this_year().strftime('%d-%b-%y') for _ in range(num_records)],  
        "Day of Week": [fake.day_of_week() for _ in range(num_records)],
        "Time": [random.randint(0, 23) for _ in range(num_records)],  
        "Type of Card": [random.choice(["Visa", "MasterCard"]) for _ in range(num_records)],
        "Entry Mode": [random.choice(["Tap", "PIN", "CVC"]) for _ in range(num_records)],
        "Amount": [f"£{round(random.uniform(5, 400), 2)}" for _ in range(num_records)],  
        "Type of Transaction": [random.choice(["POS", "ATM", "Online"]) for _ in range(num_records)],
        "Merchant Group": [random.choice(["Entertainment", "Services", "Restaurant", "Electronics", 
                                          "Children", "Fashion", "Gaming", "Food", "Subscription", "Products"]) 
                           for _ in range(num_records)],
        "Country of Transaction": [fake.country() for _ in range(num_records)],
        "Shipping Address": [fake.country() for _ in range(num_records)],  
        "Country of Residence": [fake.country() for _ in range(num_records)],
        "Gender": [random.choice(["M", "F"]) for _ in range(num_records)],
        "Age": [round(random.uniform(18, 85), 1) for _ in range(num_records)],  
        "Bank": [random.choice(["RBS", "Lloyds", "Barclays", "Metro", "Monzo", "HSBC", "Halifax"]) 
                 for _ in range(num_records)],
        "Fraud": [random.choice([0, 1]) for _ in range(num_records)]  
    }
    return pd.DataFrame(data)

# Generate initial data and save to CSV
if not os.path.exists(csv_file):
    df = generate_data(initial_records)
    df.to_csv(csv_file, index=False)
    print(f"Initial data generated and saved as '{csv_file}'.")

# Append new data every minute
while True:
    df_new = generate_data(interval_records)
    df_new.to_csv(csv_file, mode='a', header=False, index=False)  # Append without header
    print(f"{interval_records} new records appended to '{csv_file}'.")
    time.sleep(60)  # Wait for 1 minute
