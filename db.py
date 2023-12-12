import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def get_mongo_client():
    uri = os.getenv("MONGODB_URI")
    return MongoClient(uri, server_api=ServerApi('1'))

def test_mongo_connection():
    client = get_mongo_client()
    try:
        dbs = client.list_database_names()
        print("Databases:", dbs)
        return True
    except Exception as e:
        print(f"MongoDB Connection Error: {e}")
        return False
