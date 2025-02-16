from motor.motor_asyncio import AsyncIOMotorClient
from config import config

# Initialize MongoDB client
client = AsyncIOMotorClient(config.MONGO_URI)
db = client.event_db  # Reference to the database
events_collection = db.events  # Reference to the "events" collection
