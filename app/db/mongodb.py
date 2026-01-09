from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()   # 🔴 THIS LINE IS REQUIRED

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise Exception("MONGO_URL not found in environment variables")

client = AsyncIOMotorClient(MONGO_URL)
db = client["searchkaro_db"]

user_collection = db["users"]
category_collection = db["categories"]
report_collection = db["reports"]