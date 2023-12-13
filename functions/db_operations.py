import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Function to get MongoDB client
def get_mongo_client():
    uri = os.getenv("MONGODB_URI")
    return MongoClient(uri, server_api=ServerApi('1'))

# Function to read data from MongoDB
def read_db():
    client = get_mongo_client()
    db = client['AssistantsData']
    collection = db['Assistants']
    try:
        data = collection.find_one()  # Adjust this based on how you want to query data
        return data if data else {}
    except Exception as e:
        print(f"Error reading from MongoDB: {e}")
        return {}

# Function to write data to MongoDB
def write_db(new_data):
    client = get_mongo_client()
    db = client['AssistantsData']
    collection = db['Assistants']
    try:
        # Modify this based on whether you want to insert new documents or update existing ones
        collection.update_one({}, {'$set': new_data}, upsert=True)
        print("Database updated.")
    except Exception as e:
        print(f"Error updating MongoDB: {e}")

def w_dbin(data):
    try:
        with open('db_instructions.json', 'w') as file:
            json.dump(data, file, indent=8)
        print("Database updated. w_dbin")
    except Exception as e:
        print(f"Error updating database w_dbin: {e}")

def r_dbin():
    try:
        with open('db_instructions.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("db_instructions.json.json not found, creating a new one.")
        return {}

def w_udbin(data):
    try:
        with open('usdb.json', 'w') as file:
            json.dump(data, file, indent=8)
        print("Database updated. w_dbin")
    except Exception as e:
        print(f"Error updating database w_dbin: {e}")

def r_udbin():
    try:
        with open('usdb.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("usdb.json not found, creating a new one.")
        return {}
    
    return message_id