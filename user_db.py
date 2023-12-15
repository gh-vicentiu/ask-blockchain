# user_db.py

from db import get_mongo_client
import uuid

def check_login(username, password):
    """
    Checks the login credentials of a user.
    Returns True if credentials are correct, False otherwise.
    """
    client = get_mongo_client()
    db = client['user_database']
    users = db['users']
    
    user = users.find_one({"username": username, "password": password})
    return bool(user)

def register_user(username, password):
    """
    Registers a new user in the MongoDB database.
    Returns the user_id if successful, False otherwise.
    """
    client = get_mongo_client()
    db = client['user_database']
    users = db['users']

    if users.find_one({"_id": username}):
        return False  # User already exists

    user_id = generate_user_id()
    try:
        users.insert_one({"_id": user_id, "username": username, "password": password})
        return user_id
    except Exception as e:
        print(f"Error in register_user: {e}")
        return False

def generate_user_id():
    """
    Generates a unique user ID.
    """
    return f"{uuid.uuid4().hex[:4]}_{uuid.uuid4().hex[:4]}"
