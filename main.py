# main.py
import sys
import json
import asyncio
import process_user
import logging
from functions.db_operations import read_db_async, write_db_async, w_dbin, r_dbin  # To handle database operations asynchronously

async def main():
    input_json = sys.argv[1]
    input_data = json.loads(input_json)
    user_id = input_data['user_id']
    messaged_us = input_data['messaged_us']

    # Assuming process_user.process_user is converted to an async function
    response = await process_user.process_user_async(user_id, messaged_us)
    print(f"Response: {response}")

if __name__ == "__main__":
    # Setup logging as before

    # Run the async main function
    asyncio.run(main())
