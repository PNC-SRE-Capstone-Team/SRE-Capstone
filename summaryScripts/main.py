from pymongo import MongoClient
import mysql.connector
from environs import Env
import time
from datetime import datetime, timedelta
import csv
import summary_builder
import query_builder

#init env
env = Env()
env.read_env()

cluster = env.str("CLUSTER_IP")

mongo_uri = env.str("MONGO_URI")


mysql_port = env.str("MYSQL_PORT")
mysql_user = env.str("MYSQL_USER")
mysql_pw = env.str("MYSQL_PW")

# Mongo DB Connection
mongo = MongoClient(mongo_uri)
mongo_db = mongo["test"]
collection = mongo_db["logs"]

# MySQL Connection

sql = mysql.connector.connect(
    host=cluster,
    user=mysql_user,
    password=mysql_pw,
    port=mysql_port,
    collation="utf8mb4_general_ci",
    database="maria_appDB"
)

if sql.is_connected():
    print("Connected to MySQL")

cursor = sql.cursor()

# while loop that will only trigger every hour
while True:
    now = datetime.now()

    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    sleep_time = (next_hour - now).total_seconds()

    time.sleep(sleep_time)

    #test summary builder
    docs = collection.find({})
    summaries = summary_builder.build_summaries(docs)

    #test query builder
    try:
        sql.start_transaction()

        cursor.execute("DELETE FROM transaction_summaries")

        transacton_query, transaction_data = query_builder.build_query(summaries[0])
        fraud_query, fraud_data = query_builder.build_query(summaries[1])

        cursor.execute(transacton_query, transaction_data)
        cursor.execute(fraud_query, fraud_data)

        sql.commit()
        print("INSERT successful")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sql.rollback()

    cursor.execute("SELECT * FROM transaction_summaries")
    res = cursor.fetchall()
    for row in res:
        print(row)

    print("Executed at: " + str(datetime.now()))

cursor.close()
sql.close()

