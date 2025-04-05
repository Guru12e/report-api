from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("DATABASE_URL"))
database = client["Astrokids"]
collection = database["ChildDetails"]

def getChildDetails():
    try:
        child_details = list(collection.find())
        print(child_details)
    except Exception as e:
        print(f"Error retrieving child details: {e}")
        return []