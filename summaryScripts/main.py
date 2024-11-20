from pymongo import MongoClient
import mysql.connector
import os
import time
from datetime import datetime, timedelta, timezone
import summary_builder
import query_builder
import logging


#init env
mongo_uri = os.getenv("MONGO_URI")

mysql_port = os.getenv("MYSQL_PORT")
mysql_user = os.getenv("MYSQL_USER")
mysql_pw = os.getenv("MYSQL_PW")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Summary Script App Started Successfully!")

# while loop that will only trigger every hour
while True:
    now = datetime.now(timezone.utc)

    date = now.date()
    timestamp = now.time()

    #set start and stop for mongo filter
    time_start = str((now - timedelta(minutes=5)).time())
    time_end = str(timestamp)
    date_string = str(date)

    next_task = (now + timedelta(minutes=5))
    sleep_time = (next_task - now).total_seconds()

    #establish mongo connection
    mongo = MongoClient(mongo_uri)
    mongo_db = mongo["prod"]
    collection = mongo_db["logs"]

    #summary builder
    find_query = {"Date": date_string, "Time": {"$gte": time_start, "$lt": time_end}}
    count = collection.count_documents(find_query)
    if count == 0:
        logging.warning("No documents found in this time window")
        logging.info("Starting 5 minute sleep cycle")
        time.sleep(sleep_time)
        continue
    
    docs = collection.find(find_query)
    summaries = summary_builder.build_summaries(docs)

    #establish connection and cursor
    sql = mysql.connector.connect(
        host="mariadb.database.svc.cluster.local",
        user=mysql_user,
        password=mysql_pw,
        port=mysql_port,
        collation="utf8mb4_general_ci",
        database="maria_appDB"
    )

    if sql.is_connected():
        logging.info("Connected to MySQL")

    cursor = sql.cursor()

    #query builder
    try:
        sql.start_transaction()

        transacton_query, transaction_data = query_builder.build_query(summaries[0])
        fraud_query, fraud_data = query_builder.build_query(summaries[1])

        cursor.execute(transacton_query, transaction_data)
        cursor.execute(fraud_query, fraud_data)

        res = cursor.fetchall()
        for row in res:
            logging.info(row)

        sql.commit()
        logging.info("INSERT successful")
        
    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")
        sql.rollback()
    
    finally:
        cursor.close()
        sql.close()
        mongo.close()

    logging.info("Executed at: " + str(datetime.now()))

    logging.info("Starting 5 minute sleep cycle")
    time.sleep(sleep_time)

