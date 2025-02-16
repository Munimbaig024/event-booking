from pymongo import MongoClient
from config import config

# Connect to MongoDB
client = MongoClient(config.MONGO_URI)
db = client["notification_db"]

# Collection for notifications
notification_collection = db["notifications"]
