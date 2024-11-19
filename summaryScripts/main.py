from pymongo import MongoClient
import mysql.connector
from environs import Env
import time
from datetime import datetime, timedelta, timezone
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

    time.sleep(sleep_time)

    #establish mongo connection
    mongo = MongoClient(mongo_uri)
    mongo_db = mongo["prod"]
    collection = mongo_db["logs"]

    #summary builder
    docs = collection.find({"Date": date_string, "Time": {"$gte": time_start, "$lt": time_end}})
    if not docs:
        print("No documents found in this time window")
        continue
    summaries = summary_builder.build_summaries(docs)

    #establish connection and cursor
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

    #query builder
    try:
        sql.start_transaction()

        transacton_query, transaction_data = query_builder.build_query(summaries[0])
        fraud_query, fraud_data = query_builder.build_query(summaries[1])

        cursor.execute(transacton_query, transaction_data)
        cursor.execute(fraud_query, fraud_data)

        res = cursor.fetchall()
        for row in res:
            print(row)

        sql.commit()
        print("INSERT successful")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sql.rollback()
    
    finally:
        cursor.close()
        sql.close()
        mongo.close()

    print("Executed at: " + str(datetime.now()))

