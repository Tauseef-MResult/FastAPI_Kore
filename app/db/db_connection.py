from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.helpers.logger_setup import logger
import os

uri = os.getenv("MONGO_URI")

try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    logger.info("Connected to MongoDB successfully")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    client = None  # Set to None to prevent unintended usage


if client:
    db = client.idea_chatbot
    users_collection = db.users
    ideas_collection = db.ideas
    counters_collection = db.counters
    evaluations_collection = db.evaluations