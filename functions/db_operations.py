import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Function to get MongoDB client
def get_mongo_client():
    uri = os.getenv("MONGODB_URI")
    return MongoClient(uri, server_api=ServerApi('1'))

# Function to read data from MongoDB
def read_db_chats():
    client = get_mongo_client()
    db = client['AssistantsData']
    collection = db['Chats']
    try:
        data = collection.find_one()  # Adjust this based on how you want to query data
        return data if data else {}
    except Exception as e:
        print(f"Error reading from MongoDB: {e}")
        return {}

# Function to write data to MongoDB
def write_db_chats(new_data):
    client = get_mongo_client()
    db = client['AssistantsData']
    collection = db['Chats']
    try:
        # Modify this based on whether you want to insert new documents or update existing ones
        collection.update_one({}, {'$set': new_data}, upsert=True)
        print("Database updated.")
    except Exception as e:
        print(f"Error updating MongoDB: {e}")

def read_db_agents():
    client = get_mongo_client()
    db = client['AssistantsData']
    collection = db['Agents']
    try:
        data = collection.find_one()  # Adjust this based on how you want to query data
        return data if data else {}
    except Exception as e:
        print(f"Error reading from MongoDB: {e}")
        return {}

# Function to write data to MongoDB
def write_db_agents(new_data):
    client = get_mongo_client()
    db = client['AssistantsData']
    collection = db['Agents']
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

def save_to_db(data, db_name='user_database', collection_name='user_paths'):
    client = get_mongo_client()
    db = client[db_name]
    collection = db[collection_name]
    for user_id, paths in data.items():
        collection.update_one({"_id": user_id}, {"$set": paths}, upsert=True)

# Load data from MongoDB
def load_from_db(db_name='user_database', collection_name='user_paths'):
    client = get_mongo_client()
    db = client[db_name]
    collection = db[collection_name]
    result = collection.find({})
    data = {item['_id']: item for item in result}
    return data