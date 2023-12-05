# process_user.py
#filename process_user.py - keep this comment always
import time
import json
import logging
import openai  # Import the OpenAI library for AI-related operations

# Importing necessary functions from other modules
from ai_make.create_ai import create_assistant  # To create a new AI assistant
from ai_make.create_thread import create_thread  # To create a new conversation thread
from ai_run.send_mess import add_message_to_thread  # To add a message to a conversation thread
from ai_run.run_ai import run_assistant  # To run the AI assistant within a thread
from functions.db_operations import read_db, write_db,w_dbin,r_dbin  # To handle database operations
from functions.ai_parse_response import ai_parse_response

# Configure basic logging to track application activity and errors


# Initialize the OpenAI client with the necessary API key
client = openai.Client()

# Main function to process a user message
def process_user(user_id, messaged_us):
    # Log the incoming user ID and message
    logging.info(f"Processing user: {user_id} with message: {messaged_us}")
    # Read the current state of the database
    db = read_db()

    # Initialize variable for the full thread
    thread_full = None
    last_assistant_id = None
    ids = 'a'

    # Check if the user ID exists in the database; if not, create a new entry
    if user_id not in db:
        logging.info(f"User {user_id} NOT found, creating a new entry.")
        db[user_id] = {}
        db[user_id][ids] = {}
        write_db(db)
    logging.info(f"User {user_id} found, proceed")
    
    # Retrieve or create an assistant ID for the user
    assistant_id = db[user_id][ids].get('last_assistant_id')
    if not assistant_id:
        logging.info(f"Creating new assistant for the user {user_id}.")
        assistant = create_assistant("relay")
        assistant_id = assistant.id
        db[user_id][ids]['last_assistant_id'] = assistant_id
        db[user_id][assistant_id] = {}
        write_db(db)
    logging.info(f"Assistant {assistant_id} for {user_id}.")
    
    # Retrieve or create a thread ID for the conversation
    thread_id = db[user_id][ids].get('last_thread_id')
    if not thread_id:
        logging.info(f"Creating new thread for the user {user_id}.")
        thread_id = create_thread()
        db[user_id][ids]['last_thread_id'] = thread_id
        db[user_id][assistant_id][thread_id] = {}
        write_db(db)
    logging.info(f"Thread {thread_id} for {user_id}.")




    
    logging.info(f"Adding Message to  {assistant_id} - {thread_id} for {user_id}.")
    message_u_id = add_message_to_thread(thread_id, messaged_us, role='user')

    if message_u_id is None:
        logging.error("Failed to add message to thread.")
        get_runs = client.beta.threads.runs.list(thread_id=thread_id, limit=1, order='desc')
        run_id = get_runs.data[0].id
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)  
        if run_status.status not in ['completed', 'failed', 'cancelled']:   
            cancel_job = client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)
            time.sleep(2)
        message_u_id = add_message_to_thread(thread_id, messaged_us, role='user')

    logging.info(f"Message {message_u_id} added to  {assistant_id} - {thread_id} for {user_id}.")

    #logging.info(f"{db[user_id][assistant_id][thread_id][message_u_id]}")
    #logging.info(f"{db[user_id][assistant_id][thread_id][message_u_id][0] = {"sent": {"role": "user", "content": messaged_us, "timestamp": int(time.time())}}}")
    
    db[user_id][assistant_id][thread_id][message_u_id] = {}
    db[user_id][assistant_id][thread_id][message_u_id][0] = {"sent": {"role": "user", "content": messaged_us, "timestamp": int(time.time())}}
    write_db(db)
      

    # Run the assistant to process the thread and get a response
    logging.info(f"Start Main Assistent: 'u_bot_0_id': {user_id}, 'a_bot_0_id': {assistant_id}, 't_bot_0_id': {thread_id}, 'm_bot_0_id': {message_u_id}, 'agent': None")
    thread_main = {'u_bot_0_id': user_id, 'a_bot_0_id': assistant_id, 't_bot_0_id': thread_id, 'm_bot_0_id': message_u_id, 'agent': None}
    thread_full = run_assistant(thread_main)
    ai_replay = ai_parse_response(thread_full)
    # Return the full conversation threads
    db[user_id][assistant_id][thread_id][message_u_id][1] = {"replay": {"role": "assistant", "content": ai_replay, "timestamp": int(time.time())}}
    write_db(db)
    return ai_replay

# This block allows the script to be run as a standalone Python script for testing
if __name__ == "__main__":
    import sys

    # Retrieve command line arguments for user ID and message
    user_id = sys.argv[1]
    messaged_us = json.loads(sys.argv[2])['message']

    # Process the user's message and print the result
    thread_full = process_user(user_id, messaged_us)
    print(f"Process result: {ai_replay}")
