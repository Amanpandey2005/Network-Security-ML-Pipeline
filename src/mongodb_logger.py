from pymongo import MongoClient
from datetime import datetime

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")

db = client["network_ids"]

collection = db["threat_logs"]

def log_threat(data):

    try:

        data["logged_at"] = str(datetime.now())

        collection.insert_one(data)

        print("Threat Logged to MongoDB")

    except Exception as e:

        print("MongoDB Error:", e)