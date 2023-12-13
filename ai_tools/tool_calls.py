#ai_tools/tool_calls.py

import json
import subprocess
import os
import time
from flask import jsonify  # Import Flask jsonify for returning JSON responses
from .main_tools import call_agent_webhook, call_agent_coder 
from .secondary_tools import create_file, execute_file, move_files
from .route_creation import add_dynamic_route, create_route_handler
from functions.return_response import send_message_to_hook

def handle_add_route(arguments, thread_main, tool_outputs, action_id):
    # Ensure arguments contain 'route' and 'file_path'
    if 'route' in arguments and 'file_path' in arguments:
        # Add the dynamic route
        add_dynamic_route(arguments['route'], arguments['file_path'])

        # Prepare a success output
        output = f"Dynamic route '{arguments['route']}' added successfully."
        tool_outputs.append({"tool_call_id": action_id, "output": output})

        # Optionally, you might want to send a message or log the action
        # send_message_to_hook(user_id=thread_main['u_bot_0_id'], messaged_back=(f"'{output}'"))

        return output
    else:
        # Handle missing arguments
        error_message = "Error: Missing 'route' or 'file_path' in arguments."
        tool_outputs.append({"tool_call_id": action_id, "output": error_message})
        # Optionally log the error or send a message
        return error_message

def handle_call_agent_webhook(arguments, thread_main, tool_outputs, action_id):
    output = call_agent_webhook(**arguments, thread_main=thread_main)
    tool_outputs.append({"tool_call_id": action_id, "output": output})  # Corrected here
    #db_entry.update({"tool": {'instruction': arguments, "timestamp": int(time.time())}})
    return output

def handle_call_agent_coder(arguments, thread_main, tool_outputs, action_id):
    output = call_agent_coder(**arguments, thread_main=thread_main)
    tool_outputs.append({"tool_call_id": action_id, "output": output})  # Corrected here
    #db_entry.update({"tool": {'instruction': arguments, "timestamp": int(time.time())}})
    return output

def handle_create_file(arguments, thread_main, tool_outputs, action_id):
    output = create_file(**arguments)
    tool_outputs.append({"tool_call_id": action_id, "output": output})  # Corrected here
    result = send_message_to_hook(user_id=thread_main['u_bot_0_id'], messaged_back=(f"'{output}'"))
    #db_entry.update({"tool": {'instruction': arguments, "timestamp": int(time.time())}})
    return output

def handle_execute_file(arguments, thread_main, tool_outputs, action_id):
    output = execute_file(**arguments)
    tool_outputs.append({"tool_call_id": action_id, "output": output})  # Corrected here
    #db_entry.update({"tool": {'instruction': arguments, "timestamp": int(time.time())}})
    return output

def handle_move_files(arguments, thread_main, tool_outputs, action_id):
    if 'fileMoves' in arguments:
        output = move_files(file_moves=arguments['fileMoves'])
        output_str = '\n'.join(output)
        tool_outputs.append({"tool_call_id": action_id, "output": output_str})  # Corrected here
        #db_entry.update({"tool": {'instruction': arguments, "timestamp": int(time.time())}})
        return output_str
    else:
        logging.error("'fileMoves' key not found in arguments for 'move_files' function.")
        return None
