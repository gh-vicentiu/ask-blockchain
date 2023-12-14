import os
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

async def get_mongo_client():
    uri = 'mongodb+srv://umbrellatechnologies:3DBGDlaFkuWFJKS5@btc-ask-cluster.jmqllnj.mongodb.net/?retryWrites=true&w=majority'
    return AsyncIOMotorClient(uri, server_api=ServerApi('1'))

async def read_db_async():
    client = await get_mongo_client()
    db = client['AssistantsData']
    collection = db['Assistants']
    try:
        data = await collection.find_one()  # Adjust based on how you want to query data
        return data if data else {}
    except Exception as e:
        print(f"Error reading from MongoDB: {e}")
        return {}

async def write_db_async(new_data):
    client = await get_mongo_client()
    db = client['AssistantsData']
    collection = db['Assistants']
    try:
        await collection.update_one({}, {'$set': new_data}, upsert=True)
        print("Database updated.")
    except Exception as e:
        print(f"Error updating MongoDB: {e}")

async def w_dbin(data):
    loop = asyncio.get_running_loop()
    try:
        await loop.run_in_executor(None, lambda: json.dump(data, open('db_instructions.json', 'w'), indent=8))
        print("Database updated. w_dbin")
    except Exception as e:
        print(f"Error updating database w_dbin: {e}")

async def r_dbin():
    loop = asyncio.get_running_loop()
    try:
        return await loop.run_in_executor(None, lambda: json.load(open('db_instructions.json', 'r')))
    except FileNotFoundError:
        print("db_instructions.json.json not found, creating a new one.")
        return {}

async def w_udbin(data):
    loop = asyncio.get_running_loop()
    try:
        await loop.run_in_executor(None, lambda: json.dump(data, open('usdb.json', 'w'), indent=8))
        print("Database updated. w_dbin")
    except Exception as e:
        print(f"Error updating database w_dbin: {e}")

async def r_udbin():
    loop = asyncio.get_running_loop()
    try:
        return await loop.run_in_executor(None, lambda: json.load(open('usdb.json', 'r')))
    except FileNotFoundError:
        print("usdb.json not found, creating a new one.")
        return {}
