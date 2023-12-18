#ai_tools/tool_calls.py

import json
import subprocess
import os
import time
from flask import jsonify  # Import Flask jsonify for returning JSON responses
from .main_tools import call_agent_webhook, call_agent_coder 
from .secondary_tools import create_file, execute_file, move_files
from .route_tools import add_to_webhook, test_webhook, remove_webhook, edit_webhook
from functions.return_response import send_message_to_hook


def handle_add_to_webhook(arguments, thread_main, tool_outputs, action_id):
    output = add_to_webhook(**arguments, user_id = thread_main['u_bot_0_id'])
    tool_outputs.append({"tool_call_id": action_id, "output": json.dumps(output)})
    #tool_outputs.append({"tool_call_id": action_id, "output": output})  # Corrected here
    #db_entry.update({"tool": {'instruction': arguments, "timestamp": int(time.time())}})
    return output

def handle_test_webhook(arguments, thread_main, tool_outputs, action_id):
    output = test_webhook(**arguments)
    tool_outputs.append({"tool_call_id": action_id, "output": json.dumps(output)})  # Corrected here
    #db_entry.update({"tool": {'instruction': arguments, "timestamp": int(time.time())}})
    return output

def handle_remove_webhook(arguments, thread_main, tool_outputs, action_id):
    output = remove_webhook(**arguments, user_id = thread_main['u_bot_0_id'])
    tool_outputs.append({"tool_call_id": action_id, "output": output})  # Corrected here
    #db_entry.update({"tool": {'instruction': arguments, "timestamp": int(time.time())}})
    return output

def handle_edit_webhook(arguments, thread_main, tool_outputs, action_id):
    output = edit_webhook(**arguments, user_id = thread_main['u_bot_0_id'])
    tool_outputs.append({"tool_call_id": action_id, "output": output})  # Corrected here
    #db_entry.update({"tool": {'instruction': arguments, "timestamp": int(time.time())}})
    return output


def handle_call_agent_webhook(arguments, thread_main, tool_outputs, action_id):
    output = call_agent_webhook(**arguments, thread_main=thread_main)
    tool_outputs.append({"tool_call_id": action_id, "output": output})  # Corrected here
    #db_entry.update({"tool": {'instruction': arguments, "timestamp": int(time.time())}})
    return output

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
    output = create_file(**arguments, user_id=thread_main['u_bot_0_id'])
    tool_outputs.append({"tool_call_id": action_id, "output": output})  # Corrected here
    result = send_message_to_hook(user_id=thread_main['u_bot_0_id'], messaged_back=(f"'{output}'"))
    #db_entry.update({"tool": {'instruction': arguments, "timestamp": int(time.time())}})
    return output

def handle_execute_file(arguments, thread_main, tool_outputs, action_id):
    output = execute_file(**arguments, user_id=thread_main['u_bot_0_id'])
    tool_outputs.append({"tool_call_id": action_id, "output": output})  # Corrected here
    #db_entry.update({"tool": {'instruction': arguments, "timestamp": int(time.time())}})
    return output

def handle_move_files(arguments, thread_main, tool_outputs, action_id):
    if 'fileMoves' in arguments:
        output = move_files(file_moves=arguments['fileMoves'], user_id=thread_main['u_bot_0_id'])
        output_str = '\n'.join(output)
        tool_outputs.append({"tool_call_id": action_id, "output": output_str})  # Corrected here
        #db_entry.update({"tool": {'instruction': arguments, "timestamp": int(time.time())}})
        return output_str
    else:
        logging.error("'fileMoves' key not found in arguments for 'move_files' function.")
        return None
