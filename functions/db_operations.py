import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Function to get MongoDB client
def get_mongo_client():
    uri = os.getenv("MONGODB_URI")
    return MongoClient(uri, server_api=ServerApi('1'))

# Function to read data from MongoDB
def read_db_chats(user_id):
    client = get_mongo_client()
    db = client['AssistantsData']
    collection = db['Chats']
    try:
        # Fetching data based on user_id
        data = collection.find_one({"_id": user_id})
        return data if data else {}
    except Exception as e:
        print(f"Error reading from MongoDB for user {user_id}: {e}")
        return {}

def write_db_chats(user_id, new_data):
    client = get_mongo_client()
    db = client['AssistantsData']
    collection = db['Chats']
    try:
        # Setting the user_id as the _id of the document
        collection.update_one({'_id': user_id}, {'$set': new_data}, upsert=True)
        print("Database updated for user:", user_id)
    except Exception as e:
        print(f"Error updating MongoDB for user {user_id}: {e}")



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
def write_db_agents(agent_id, new_data):
    client = get_mongo_client()
    db = client['AssistantsData']
    collection = db['Agents']
    try:
        # Assuming agent_id is analogous to user_id for agent documents
        collection.update_one({'_id': agent_id}, {'$set': new_data}, upsert=True)
        print("Database updated for agent:", agent_id)
    except Exception as e:
        print(f"Error updating MongoDB for agent {agent_id}: {e}")


def save_to_db(data, db_name='user_database', collection_name='user_paths'):
    client = get_mongo_client()
    db = client[db_name]
    collection = db[collection_name]
    for user_id, paths in data.items():
        document = {"_id": user_id, **paths}  # Unpack paths directly into the document
        collection.update_one({"_id": user_id}, {"$set": document}, upsert=True)


def load_from_db(db_name='user_database', collection_name='user_paths'):
    client = get_mongo_client()
    db = client[db_name]
    collection = db[collection_name]
    result = collection.find({})
    data = {}
    for item in result:
        user_id = item.pop('_id', None)
        if user_id:
            data[user_id] = {k: v for k, v in item.items() if isinstance(v, dict)}
    return data


def get_user_paths(user_id, db_name='user_database', collection_name='user_paths'):
    client = get_mongo_client()
    db = client[db_name]
    collection = db[collection_name]
    result = collection.find_one({"_id": user_id})

    if result:
        result.pop('_id', None)  # Remove the '_id' field
        links = []
        for path_id, path_info in result.items():
            if isinstance(path_info, dict):
                script_path = path_info.get("script_path", "")
                hook_name = path_info.get("hook_name", "Unnamed Hook")
                hook_description = path_info.get("hook_description", "No Description")
                file_exists = os.path.exists(script_path)
                link = (f'<a href="/webhook/{user_id}/{path_id}" target="_blank">{hook_name}</a> '
                        f'(Description: {hook_description}, Exists: {file_exists})')
                links.append(link)
        return links
    return None
