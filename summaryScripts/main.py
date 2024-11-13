import pymongo
import mysql.connector
from environs import Env

#init env
env = Env()
env.read_env()

cluster = env.str("CLUSTER_IP")

mongo_port = env.str("MONGO_URI")


mysql_port = env.str("MYSQL_PORT")
mysql_user = env.str("MYSQL_USER")
mysql_pw = env.str("MYSQL_PW")

# TODO GET COLLECTIONS

