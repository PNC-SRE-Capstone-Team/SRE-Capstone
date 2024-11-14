from faker import Faker
import pandas as pd
import random

# Initialize Faker
fake = Faker()

# Set the number of records to generate
num_records = 1000


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
    "Age": [round(random.uniform(18, 85), 1) for _ in range(num_records)],  # Rounded age with decimal
    "Bank": [random.choice(["RBS", "Lloyds", "Barclays", "Metro", "Monzo", "HSBC", "Halifax"]) 
             for _ in range(num_records)],
    "Fraud": [random.choice([0, 1]) for _ in range(num_records)]  
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV file
df.to_csv("FakeCreditCardDataNew.csv", index=False)

print("Fake data generated and saved as 'FakeCreditCardData.csv'.")
