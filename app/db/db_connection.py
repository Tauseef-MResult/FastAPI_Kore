from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

uri = os.getenv("MONGO_URI")

try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    print("Connected to MongoDB successfully")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    client = None  # Set to None to prevent unintended usage


if client:
    db = client.idea_chatbot
    users_collection = db.users
    ideas_collection = db.ideas
    counters_collection = db.counters