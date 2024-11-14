from pymongo import MongoClient
import mysql.connector
from environs import Env

#init env
env = Env()
env.read_env()

cluster = env.str("CLUSTER_IP")

mongo_uri = env.str("MONGO_URI")


mysql_port = env.str("MYSQL_PORT")
mysql_user = env.str("MYSQL_USER")
mysql_pw = env.str("MYSQL_PW")

# TODO GET COLLECTIONS
mongo = MongoClient(mongo_uri)
mongo_db = mongo["local"]
collections = mongo_db.list_collection_names()
print(collections)

# TODO build summaries for all entries and just fraud

# total of each card type JSON
# total of each entry mode JSON
# average amount float
# total of each transaction type JSON
# total country of transaction JSON
# total shipping address countries  JSON
# total Country of residence JSON
# total of each bank JSON
# fraud count
