# process_bot.py
#filename process_bot.py - keep this comment always
import time
import json
import logging
import openai  # Import the OpenAI library for AI-related operations

# Importing necessary functions from other modules
from ai_make.create_ai import create_assistant
from ai_make.create_thread import create_thread  # To create a new conversation thread
from ai_run.send_mess import add_message_to_thread  # To add a message to a conversation thread
from ai_run.run_ai import run_assistant  # To run the AI assistant within a thread
from functions.db_operations import read_db, write_db,w_dbin,r_dbin  # To handle database operations
from functions.ai_parse_response import ai_parse_response

# Configure basic logging to track application activity and errors
# Initialize the OpenAI client with the necessary API key
client = openai.Client()
# Read the current state of the database
db = read_db()

# Main function to process a user message
def process_bot(instruction, thread_main):
    print('xxx')
    print(thread_main)
    print('xxx')

    # Log the incoming user ID and message
    logging.info(f"Processing bot: {thread_main['u_bot_0_id']} with message: {instruction}")

    # Initialize variable for the full thread
    thread_full = None

    ids = 'a'

    # Retrieve or create an assistant ID for the bot
    assistant_id = db[thread_main['u_bot_0_id']][ids].get(thread_main['agent'] + '_assistant_id')
    if not assistant_id:
        logging.info(f"Creating new assistant for {thread_main['agent']}.")
        assistant = create_assistant(thread_main['agent'])
        assistant_id = assistant.id
        db[thread_main['u_bot_0_id']][ids][thread_main['agent'] + "_assistant_id"] = assistant_id
        write_db(db)

    # Retrieve or create a thread ID for the conversation
    thread_id = db[thread_main['u_bot_0_id']][ids].get(thread_main['agent'] + '_thread_id')
    if not thread_id:
        logging.info(f"Creating new thread for {thread_main['agent']}.")
        thread_id = create_thread()
        db[thread_main['u_bot_0_id']][ids][thread_main['agent'] + '_thread_id'] = thread_id
        db[thread_main['u_bot_0_id']][thread_main['a_bot_0_id']][thread_main['t_bot_0_id']][thread_main['m_bot_0_id']][thread_id] = {}
        write_db(db)

    message_u_id = add_message_to_thread(thread_id, instruction, role='user')
    if message_u_id is None:
        logging.error("Failed to add message to thread.")
        return None
    write_db(db)

    if message_u_id not in db[thread_main['u_bot_0_id']][thread_main['a_bot_0_id']][thread_main['t_bot_0_id']][thread_main['m_bot_0_id']]:
        db[thread_main['u_bot_0_id']][thread_main['a_bot_0_id']][thread_main['t_bot_0_id']][thread_main['m_bot_0_id']][message_u_id] = {}
    db[thread_main['u_bot_0_id']][thread_main['a_bot_0_id']][thread_main['t_bot_0_id']][thread_main['m_bot_0_id']][message_u_id]['0'] = {"sent": {"role": "user", "content": instruction, "timestamp": int(time.time())}}
    write_db(db)

    print(f"Type of message_u_id: {type(message_u_id)}")
    print(f"Nested dict access: {db[thread_main['u_bot_0_id']][thread_main['a_bot_0_id']][thread_main['t_bot_0_id']][thread_main['m_bot_0_id']]}")



    # Run the assistant to process the thread and get a response
    thread_main = {'a_bot_1_id': assistant_id, 't_bot_1_id': thread_id, 'm_bot_1_id': message_u_id, 'agent': [thread_main['agent']], 'u_bot_0_id': [thread_main['u_bot_0_id']], 'a_bot_0_id': [thread_main['a_bot_0_id']], 't_bot_0_id': [thread_main['t_bot_0_id']], 'm_bot_0_id': [thread_main['m_bot_0_id']],}
    thread_full = run_assistant(thread_main)
    ai_replay = ai_parse_response(thread_full)

    # Return the full conversation threads
    #db[thread_main['u_bot_0_id']][thread_main['a_bot_0_id']][thread_main['t_bot_0_id']][thread_main['m_bot_0_id']][message_u_id]['1'] = {"replay": {"role": "assistant", "content": ai_replay, "timestamp": int(time.time())}}
    write_db(db)

    return ai_replay


# This block allows the script to be run as a standalone Python script for testing
if __name__ == "__main__":
    import sys

    # Retrieve command line arguments for user ID and message
    user_id = sys.argv[1]
    messaged_us = json.loads(sys.argv[2])['message']

    # Process the user's message and print the result
    thread_full = process_bot(user_id, messaged_us)
    print(f"Process result: {ai_replay}")
