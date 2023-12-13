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
from functions.db_operations import read_db_chats, write_db_chats, read_db_agents, write_db_agents, w_dbin,r_dbin  # To handle database operations
from functions.ai_parse_response import ai_parse_response
from functions.return_response import send_message_to_hook


client = openai.Client()

# Main function to process a user message
def process_user(user_id, messaged_us):
    # Log the incoming user ID and message
    logging.info(f"Processing user: {user_id} with message: {messaged_us}")
    # Read the current state of the database
    dbc = read_db_chats()
    dba = read_db_agents()

    # Initialize variable for the full thread
    thread_full = None
    last_assistant_id = None
    ids = 'active'

    # Check if the user ID exists in the database; if not, create a new entry
    if user_id not in dbc:
        logging.info(f"User {user_id} NOT found, creating a new entry.")
        dbc[user_id] = {}
        dbc[user_id][ids] = {}
        write_db_chats(dbc)
    logging.info(f"User {user_id} found, proceed")
    
    if ids not in dba:
        dba[ids] = {}

    # Retrieve or create an assistant ID for the user
    assistant_id = dba[ids].get('relay_assistant_id')
    if not assistant_id:
        logging.info(f"Creating new global assistant.")
        assistant = create_assistant("relay")
        assistant_id = assistant.id
        dba[ids]['relay_assistant_id'] = assistant_id
        write_db_agents(dba)
    logging.info(f"Assistant {assistant_id} for {user_id}.")
    
    # Ensure that the assistant ID key exists in the dbc[user_id] dictionary
    if assistant_id not in dbc[user_id]:
        dbc[user_id][assistant_id] = {}
        write_db_chats(dbc)
    
    # Retrieve or create a thread ID for the conversation
    thread_id = dbc[user_id][ids].get('active_relay_thread_id')
    if not thread_id:
        logging.info(f"Creating new thread for the user {user_id}.")
        thread_id = create_thread()
        dbc[user_id][ids]['active_relay_thread_id'] = thread_id
        dbc[user_id][assistant_id][thread_id] = {}
        write_db_chats(dbc)
    logging.info(f"Thread {thread_id} for {user_id}.")

    
    logging.info(f"Adding Message to  {assistant_id} - {thread_id} for {user_id}.")
    message_u_id = add_message_to_thread(thread_id, messaged_us, role='user', agent=None)
   


    logging.info(f"Message {message_u_id} added to  {assistant_id} - {thread_id} for {user_id}.")

    #logging.info(f"{db[user_id][assistant_id][thread_id][message_u_id]}")
    #logging.info(f"{db[user_id][assistant_id][thread_id][message_u_id][0] = {"sent": {"role": "user", "content": messaged_us, "timestamp": int(time.time())}}}")
    

    if message_u_id not in dbc[user_id][assistant_id][thread_id]:
        dbc[user_id][assistant_id][thread_id][message_u_id] = {}
    dbc[user_id][assistant_id][thread_id][message_u_id]['0'] = {"sent": {"role": "user", "content": messaged_us, "timestamp": int(time.time())}}
    write_db_chats(dbc)
      

    # Run the assistant to process the thread and get a response
    logging.info(f"Start Main Assistent: 'u_bot_0_id': {user_id}, 'a_bot_0_id': {assistant_id}, 't_bot_0_id': {thread_id}, 'm_bot_0_id': {message_u_id}, 'agent': None")
    thread_main = {'u_bot_0_id': user_id, 'a_bot_0_id': assistant_id, 't_bot_0_id': thread_id, 'm_bot_0_id': message_u_id, 'agent': None}
    thread_full = run_assistant(thread_main)
    ai_replay = ai_parse_response(thread_full)
    result = send_message_to_hook(user_id, messaged_back=ai_replay)
    
    dbc = read_db_chats()
    dba = read_db_agents()
    # Return the full conversation threads
    dbc[user_id][assistant_id][thread_id][message_u_id]['1'] = {"replay": {"role": "assistant", "content": ai_replay, "timestamp": int(time.time())}}
    write_db_chats(dbc)
    return ai_replay
