from db import get_mongo_client_async  # Ensure this is the async version
import uuid
import asyncio


async def check_login_async(username, password):
    """
    Checks the login credentials of a user asynchronously.
    Returns True if credentials are correct, False otherwise.
    """
    client = await get_mongo_client_async()
    db = client['user_database']
    users = db['users']

    user = await users.find_one({"username": username, "password": password})
    return bool(user)


async def register_user_async(username, password):
    """
    Registers a new user in the MongoDB database asynchronously.
    Returns the user_id if successful, False otherwise.
    """
    client = await get_mongo_client_async()
    db = client['user_database']
    users = db['users']

    if await users.find_one({"username": username}):
        return False  # User already exists

    user_id = generate_user_id()
    try:
        await users.insert_one({"username": username, "password": password, "user_id": user_id})
        return user_id
    except Exception as e:
        print(f"Error in register_user: {e}")
        return False


def generate_user_id():
    """
    Generates a unique user ID.
    """
    return f"{uuid.uuid4().hex[:4]}_{uuid.uuid4().hex[:4]}"
