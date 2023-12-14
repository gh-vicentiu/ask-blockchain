import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

async def get_mongo_client_async():
    uri = "mongodb+srv://umbrellatechnologies:3DBGDlaFkuWFJKS5@btc-ask-cluster.jmqllnj.mongodb.net/?retryWrites=true&w=majority"
    return AsyncIOMotorClient(uri, server_api=ServerApi('1'))

async def test_mongo_connection_async():
    client = await get_mongo_client_async()
    try:
        dbs = await client.list_database_names()
        print("Databases:", dbs)
        return True
    except Exception as e:
        print(f"MongoDB Connection Error: {e}")
        return False
