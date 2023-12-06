# main.py
import sys
import json
import process_user
import logging
from functions.db_operations import read_db, write_db,w_dbin,r_dbin  # To handle database operations

# Read the current state of the database
db = read_db()


# Set up basic logging
logging.basicConfig(level=logging.INFO, filename='assistant_run.log', 
                    format='%(asctime)s:%(levelname)s:%(message)s')
                    
# Create a StreamHandler to output logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))

# Add the handler to the root logger
logging.getLogger().addHandler(console_handler)

def main():
    input_json = sys.argv[1]
    input_data = json.loads(input_json)
    user_id = input_data['user_id']
    messaged_us = input_data['messaged_us']
    response = process_user.process_user(user_id, messaged_us)
    print(f"Response: {response}")

if __name__ == "__main__":
    main()

#
#
#

# main.py
import sys
import json
import process_user
import logging
from functions.db_operations import read_db, write_db,w_dbin,r_dbin  # To handle database operations

# Read the current state of the database
db = read_db()


# Set up basic logging
logging.basicConfig(level=logging.INFO, filename='assistant_run.log', 
                    format='%(asctime)s:%(levelname)s:%(message)s')
                    
# Create a StreamHandler to output logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))

# Add the handler to the root logger
logging.getLogger().addHandler(console_handler)

def main():
    input_json = sys.argv[1]
    input_data = json.loads(input_json)
    user_id = input_data['user_id']
    messaged_us = input_data['messaged_us']
    response = process_user.process_user(user_id, messaged_us)
    print(f"Response: {response}")

if __name__ == "__main__":
    main()


#
#
#

#filename ai-make/create_ai.py - keep this comment always
import openai
import json
import logging

client = openai.Client()


def create_assistant(agent=None):
    from ai_tools.main_tools import tools_list
    from ai_tools.secondary_tools import tools_lite
    tool_list = tools_list
    tool_lite = tools_lite

    if agent == "relay":
        assistant = client.beta.assistants.create(
        name=agent,
        #instructions=("you are a relay node. use [btc_price] function to ask 'btc_price' any questions regarding bitcoin price. use [ask_blockchain] function to ask 'ask_blockchain' any questions regarding bitcoin price."),
        instructions=("You are an intention relay hub, your task is to understand what the user wants and pass properly formulated istructions to one of the 2 agents under you. sendTo 'agent_price' by using [call_agent_price] function to find out bitcoin related things. You sentTo 'agent_coder' by using [call_agent_coder] for any coding related tasks"),

        tools=tool_list,
        model="gpt-3.5-turbo-1106"        
    )
    elif agent == "agent_price":
        assistant = client.beta.assistants.create(
        name=agent,
        instructions=("you are a bitcoin price master. make up prices as you are asked"),
        model="gpt-3.5-turbo-1106"        
    )
    elif agent == "agent_coder":
        assistant = client.beta.assistants.create(
        name=agent,
        instructions=("you are a proffesional coder. you will transform incoming requests into a py script that you will execute. To do so, you can use [create_file] and [execute_file] functions, at the end save them by using [move_files]"),
        tools=tools_lite,
        model="gpt-3.5-turbo-1106"        
    )
    else:
        logging.info(agent)
        raise ValueError("Invalid agent specified")

    return assistant


if __name__ == "__main__":
    assistant = create_assistant()
    print(f"Assistant created: {assistant}")

#
#
#

#filename ai_make/create_thread.py - keep this comment always
import openai  # Make sure to import openai

client = openai.Client()  # Initialize the OpenAI client

def create_thread():
    # Make an API call to create a thread and return the thread ID
    thread_response = client.beta.threads.create()  # Adjust this line according to the actual API method
    return thread_response.id  # Assuming the response has an 'id' attribute

#
#
#

#ai_run/run_ai.py
import time
import openai
import json
import logging
from ai_tools.main_tools import call_agent_price, call_agent_coder
from ai_tools.secondary_tools import execute_file, create_file, move_files
from functions.db_operations import read_db, write_db, r_dbin, w_dbin  # To handle database operations



client = openai.Client()  # Initialize the OpenAI client
# Read the current state of the database
db = read_db()


def run_assistant(thread_main):

    if thread_main['agent'] is None:
        thread_id=thread_main['t_bot_0_id'] 
        assistant_id=thread_main['a_bot_0_id']
        message_u_id=thread_main['m_bot_0_id']
        logging.info("Starting the main assistant...")
    else:
        thread_id=thread_main['t_bot_1_id'] 
        assistant_id=thread_main['a_bot_1_id']
        message_u_id=thread_main['m_bot_1_id']
        logging.info("Starting the secondery bots...")
    user_id = thread_main['u_bot_0_id']

    
    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id, instructions="")
    logging.info("Main Assistant run initiated. Dumping initial run status:")
    #logging.info(json.dumps(run, default=str, indent=4))

    

    while True:
        logging.info("Checking run status...")
        time.sleep(3)
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        #logging.info(F"Current run status: {run_status}")
        #logging.info(json.dumps(run_status, default=str, indent=4))

        if run_status.status == 'completed':
            logging.info("Run completed. Fetching messages...")
            messages = client.beta.threads.messages.list(thread_id=thread_id, limit=1, order='desc')
            logging.info(f"Messages fetched from the thread {messages}.")
            return messages
 
        elif run_status.status == 'requires_action':
            logging.info("Function Calling")
            required_actions = run_status.required_action.submit_tool_outputs.model_dump()
            logging.info(required_actions)
            tool_outputs = []
            for action in required_actions["tool_calls"]:
                func_name = action['function']['name']
                arguments = json.loads(action['function']['arguments'])
                
                if func_name == "call_agent_price":
                    output = call_agent_price(sentTo=arguments['sentTo'], sentFrom=arguments['sentFrom'], instruction=arguments['instruction'], thread_main=thread_main)
                    tool_outputs.append({
                        "tool_call_id": action['id'],
                        "output": output,
                     })
                    
                    if thread_main['agent'] is None:
                        db[user_id][assistant_id][thread_id][message_u_id] = {}
                        db[user_id][assistant_id][thread_id][message_u_id][2] = {"tool":{'instruction': arguments, "timestamp": int(time.time())}}
                   
                    logging.info(f"Agent Sent this: {output}")
                    logging.info(json.dumps(run, default=str, indent=4))

                elif func_name == "call_agent_coder":
                    output = call_agent_coder(sentTo=arguments['sentTo'], sentFrom=arguments['sentFrom'], instruction=arguments['instruction'], thread_main=thread_main)
                    tool_outputs.append({
                        "tool_call_id": action['id'],
                        "output": output,
                     })
                    
                    if thread_main['agent'] is None:
                        db[user_id][assistant_id][thread_id][message_u_id] = {}
                        db[user_id][assistant_id][thread_id][message_u_id][2] = {"tool":{'instruction': arguments, "timestamp": int(time.time())}}
                    
                    logging.info(f"Agent Sent this: {output}")
                    logging.info(json.dumps(run, default=str, indent=4))
                
                elif func_name == "create_file":
                    output = create_file(fileName=arguments['fileName'], fileContent=arguments['fileContent'])
                    tool_outputs.append({
                        "tool_call_id": action['id'],
                        "output": output,
                     })
                    
                    if thread_main['agent'] is None:
                        db[user_id][assistant_id][thread_id][message_u_id] = {}
                        db[user_id][assistant_id][thread_id][message_u_id][2] = {"tool":{'instruction': arguments, "timestamp": int(time.time())}}
                    
                    logging.info(f"Agent Sent this: {output}")
                    logging.info(json.dumps(run, default=str, indent=4))

                elif func_name == "execute_file":
                    output = execute_file(fileName=arguments['fileName'])
                    tool_outputs.append({
                        "tool_call_id": action['id'],
                        "output": output,
                     })
                    
                    if thread_main['agent'] is None:
                        db[user_id][assistant_id][thread_id][message_u_id] = {}
                        db[user_id][assistant_id][thread_id][message_u_id][2] = {"tool":{'instruction': arguments, "timestamp": int(time.time())}}
                    
                    logging.info(f"Agent Sent this: {output}")
                    logging.info(json.dumps(run, default=str, indent=4))
                
                elif func_name == "move_files":
                    # Check if arguments is already a dictionary
                    if isinstance(arguments, str):
                        try:
                            arguments_dict = json.loads(arguments)
                        except json.JSONDecodeError as e:
                            logging.error(f"Error parsing JSON arguments for 'move_files': {e}")
                            continue
                    elif isinstance(arguments, dict):
                        arguments_dict = arguments
                    else:
                        logging.error("Unexpected arguments type for 'move_files'")
                        continue

                    if 'fileMoves' in arguments_dict:
                        output = move_files(file_moves=arguments_dict['fileMoves'])

                        # Join the list of strings into a single string
                        output_str = '\n'.join(output)

                        tool_outputs.append({
                            "tool_call_id": action['id'],
                            "output": output_str,
                        })
                        
                        if thread_main['agent'] is None:
                            db[user_id][assistant_id][thread_id][message_u_id] = {}
                            db[user_id][assistant_id][thread_id][message_u_id][2] = {"tool":{'instruction': arguments_dict, "timestamp": int(time.time())}}
                        
                        logging.info(f"Agent {agent} Sent this: {output}")
                        logging.info(json.dumps(run, default=str, indent=4))
                    else:
                        logging.error(f"'fileMoves' key not found in arguments for 'move_files' function.")
                else:
                    raise ValueError(f"Unknown function: {func_name}")

               
            print("Submitting outputs back to the Assistant...")
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

            if thread_main['agent'] is None:
                db[user_id][assistant_id][thread_id][message_u_id][3] = {"tool":{func_name: tool_outputs, "timestamp": int(time.time())}}
                write_db(db)

            logging.info(f"Submitting outputs back: {tool_outputs}")
            #logging.info(json.dumps(run, default=str, indent=4))


        elif run_status.status == 'failed':
            logging.error("Run failed. Exiting...")
            if run_status.last_error:
                # Directly access the 'message' attribute of last_error
                error_message = run_status.last_error.message if run_status.last_error.message else 'Unknown error'
                logging.error(f"Error details: {error_message}")
            return None

        else:
            logging.info("Waiting for the Assistant to process...")
            time.sleep(3)
    # Update the database with the new state

    return None


#
#
#

import openai
import logging
import json


client = openai.Client()

def add_message_to_thread(thread_id, messaged_us, role='user'):
    try:
        logging.info(f"Adding Message to thread: {messaged_us}")
        added_message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,
            content=messaged_us
        )

        # Log the message ID and its details
        logging.info(f"Message ID registered: {added_message.id}")
        logging.info(json.dumps(added_message, default=str, indent=4))

        return added_message.id

    except Exception as e:
        logging.error(f"Error in add_message_to_thread: {e}")
        # Removed the incorrect logging line referencing 'run'
        return None

#
#
#

#filename ai_tools/main_tools.py - keep this comment always
import json


def call_agent_price(sentTo, sentFrom, instruction, thread_main):
    from process_bot import process_bot
    print(f"Sending message from {sentFrom} to {sentTo}: '{instruction}'")
    thread_main['agent'] = sentTo
    response = process_bot(instruction=instruction, thread_main=thread_main)
    return f"result {response}"

def call_agent_coder(sentTo, sentFrom, instruction, thread_main):
    from process_bot import process_bot
    print(f"Sending message from {sentFrom} to {sentTo}: '{instruction}'")
    thread_main['agent'] = sentTo
    response = process_bot(instruction=instruction, thread_main=thread_main)
    return f"result {response}"

tools_list = [{
    "type": "function",
    "function": {
        "name": "call_agent_price",
        "description": "send messages using this function",
        "parameters": {
            "type": "object",
            "properties": {
                "sentTo": {
                    "type": "string",
                    "description": "message for"
                },
                "sentFrom": {
                    "type": "string",
                    "description": "message from"
                },
                "instruction": {
                    "type": "string",
                    "description": "ask your question to the btc price agent here"
                }
            },
            "required": ["sentTo", "sentFrom", "instruction"]
        }
    }
}, {
    "type": "function",
    "function": {
        "name": "call_agent_coder",
        "description": "send messages using another function",
        "parameters": {
            "type": "object",
            "properties": {
                "sentTo": {
                    "type": "string",
                    "description": "message for"
                },
                "sentFrom": {
                    "type": "string",
                    "description": "message from"
                },
                "instruction": {
                    "type": "string",
                    "description": "ask your question to another_function here"
                }
            },
            "required": ["sentTo", "sentFrom", "instruction"]
        }
    }
}]

#
#
#

import json
import subprocess
import os
import shutil

def create_file(fileName, fileContent):
    sandbox_dir = "sandbox"
    # Ensure the sandbox directory exists
    if not os.path.exists(sandbox_dir):
        os.makedirs(sandbox_dir)

    # Adjust the file path to include the sandbox directory
    filePath = os.path.join(sandbox_dir, fileName)

    try:
        with open(filePath, 'w') as file:
            file.write(fileContent)
        return f"File '{filePath}' created successfully."
    except IOError as e:
        return f"Error creating file: {e}"



def execute_file(fileName):
    sandbox_dir = "sandbox"
    # Adjust the file path to include the sandbox directory
    filePath = os.path.join(sandbox_dir, fileName)

    try:
        result = subprocess.run(['python3', filePath], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing file: {e.output}"


def save_file(fileName, ):
    
    sandbox_dir = "sandbox"
    # Ensure the sandbox directory exists
    if not os.path.exists(sandbox_dir):
        os.makedirs(sandbox_dir)

    # Adjust the file path to include the sandbox directory
    filePath = os.path.join(sandbox_dir, fileName)

    try:
        with open(filePath, 'w') as file:
            file.write(fileContent)
        return f"File '{filePath}' created successfully."
    except IOError as e:
        return f"Error creating file: {e}"



def move_files(file_moves):
    sandbox_dir = "sandbox"
    results = []

    # Ensure the sandbox directory exists
    if not os.path.exists(sandbox_dir):
        os.makedirs(sandbox_dir)

    for file_move in file_moves:
        file_name = file_move["fileName"]
        destination_subdir = file_move["destination"]

        # Ensure the target subdirectory exists
        target_dir = os.path.join(sandbox_dir, destination_subdir)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        source_path = os.path.join(sandbox_dir, file_name)
        if os.path.exists(source_path):
            destination_path = os.path.join(target_dir, file_name)
            try:
                shutil.move(source_path, destination_path)
                results.append(f"Moved '{source_path}' to '{destination_path}'")
            except IOError as e:
                results.append(f"Error moving file '{file_name}': {e}")
        else:
            results.append(f"File '{file_name}' not found in '{sandbox_dir}'")

    return results

# Example usage:
# file_moves = [
#     {"fileName": "file1.txt", "destination": "tested-working"},
#     {"fileName": "file2.txt", "destination": "tested-unworking"}
# ]
# results = move_files(file_moves)
# for result in results:
#     print(result)


tools_lite = [{
    "type": "function",
    "function": {
        "name": "create_file",
        "description": "saves to files locally",
        "parameters": {
            "type": "object",
            "properties": {
                "fileName": {
                    "type": "string",
                    "description": "give the file a name eg: filename.py"
                },
                "fileContent": {
                    "type": "string",
                    "description": "write here the content for the file"
                },
            },
            "required": ["fileName", "fileCOntent"]
        }}}, {
    "type": "function",
    "function": {
        "name": "execute_file",
        "description": "for executing py scripts",
        "parameters": {
            "type": "object",
            "properties": {
                "fileName": {
                    "type": "string",
                    "description": "provide the name of the file you want to execute: eg: fileName.py"
                }
            },
            "required": ["fileName"]
        }
    }
},{
    "type": "function",
    "function": {
        "name": "move_files",
        "description": "moves files to specified subdirectories based on individual status",
        "parameters": {
            "type": "object",
            "properties": {
                "fileMoves": {
                    "type": "array",
                    "description": "list of objects containing file names and their respective destinations",
                    "items": {
                        "type": "object",
                        "properties": {
                            "fileName": {
                                "type": "string",
                                "description": "name of the file to be moved"
                            },
                            "destination": {
                                "type": "string",
                                "enum": ["tested-working", "tested-unworking"],
                                "description": "destination subdirectory for the file ('tested-working' or 'tested-unworking')"
                            }
                        },
                        "required": ["fileName", "destination"]
                    }
                }
            },
            "required": ["fileMoves"]
        }
    }
}]
#
#
#

import logging
import json

def ai_parse_response(messages):
    if messages.data:
        latest_message = messages.data[0]  # Get the first (and only) message in the list

        if latest_message.content and isinstance(latest_message.content, list):
            first_content_item = latest_message.content[0]

            if hasattr(first_content_item, 'text') and hasattr(first_content_item.text, 'value'):
                text_value = first_content_item.text.value
                return text_value  # Return the text content of the latest message
            else:
                logging.error("Content item does not have a 'text' attribute with 'value'.")
        else:
            logging.error("Latest message content is not a list or is empty.")
    else:
        logging.info("No messages found in the thread.")

    return None

    #
    #
    #

    # db_operations.py

import json  # Add this import statement

def read_db():
    try:
        with open('iddb.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("iddb.json not found, creating a new one.")
        return {}

def deep_merge(orig_dict, new_dict):
    """
    Recursively merges new_dict into orig_dict.
    For each key in new_dict:
        - If the key is not in orig_dict, it adds the key-value pair.
        - If the key is in orig_dict and both values are dictionaries, it calls deep_merge recursively.
        - Otherwise, it updates the value in orig_dict with the value from new_dict.
    """
    for key, value in new_dict.items():
        if key in orig_dict:
            if isinstance(value, dict) and isinstance(orig_dict[key], dict):
                deep_merge(orig_dict[key], value)
            else:
                orig_dict[key] = value
        else:
            orig_dict[key] = value

def write_db(new_data):
    try:
        # Read existing data from the file
        try:
            with open('iddb.json', 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {}
            print("Database file not found. A new file will be created.")

        # Merge new data into existing data
        deep_merge(existing_data, new_data)

        # Write updated data to the file
        with open('iddb.json', 'w') as file:
            json.dump(existing_data, file, indent=8)

        print("Database updated.")
    except Exception as e:
        print(f"Error updating database: {e}")

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

    
    return message_id

    #
    #
    #

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

#
#
#
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
        get_runs = client.beta.threads.runs.list(thread_id=thread_id, limit=1, order='desc')
        run_id = get_runs.data[0].id
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)  
        if run_status.status not in ['completed', 'failed', 'cancelled']:   
            cancel_job = client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)
            message_u_id = add_message_to_thread(thread_id, instruction, role='user')
    logging.info(f"Message {message_u_id} added to  {assistant_id} - {thread_id} for {thread_main['u_bot_0_id']}.")
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
