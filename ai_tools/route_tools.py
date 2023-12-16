import requests
import json
import random
import string

def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def add_to_webhook(script_path, hook_name, hook_description, user_id):
    url = "http://127.0.0.1:5000/dohook/"
    headers = {"Content-Type": "application/json"}
    url_path = generate_random_string(8)
    
    data = {
        "user_id": user_id, 
        "path": url_path, 
        "script_path": 'sandbox/' + user_id + '/' + script_path, 
        "hook_name": hook_name, 
        "hook_description": hook_description
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("success"):
            print(f"Webhook '/webhook/{user_id}/{url_path}' added successfully with script path '{script_path}'")
            return f"Success: Webhook '/webhook/{user_id}/{url_path}' added"
        else:
            print(f"Error adding webhook:", response_data.get("error"))
            return f"Error adding webhook:", response_data.get("error")
    else:
        print("HTTP POST request failed with status code:", response.status_code)
        return f"HTTP POST request failed with status code: {response.status_code}"

def test_webhook(url_path):
    base_url = "http://127.0.0.1:5000/"
    full_url = f"{base_url}{url_path}"

    try:
        response = requests.get(full_url)
        if response.status_code == 200:
            print(f"Webhook '{full_url}' tested successfully.")
            return f"Success: Webhook '{full_url}' is up and running. Result: {response.text}"
        else:
            print(f"Webhook test failed with status code: {response.status_code}")
            return f"Error: Webhook test failed with status code: {response.status_code}. Details: {response.text}"
    except Exception as e:
        print(f"Error testing webhook: {e}")
        return f"Error: Could not test webhook. Exception: {str(e)}"


def remove_webhook(path_id, user_id):
    url = f"http://127.0.0.1:5000/remove_user_paths/{user_id}/{path_id}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success"):
                print(f"Webhook with path_id '{path_id}' for user '{user_id}' removed successfully.")
                return f"Success: Webhook with path_id '{path_id}' for user '{user_id}' removed."
            else:
                print(f"Failed to remove webhook: {response_data.get('error', 'Unknown Error')}")
                return f"Error removing webhook: {response_data.get('error', 'Unknown Error')}"
        else:
            print(f"HTTP POST request failed with status code: {response.status_code}")
            return f"HTTP POST request failed with status code: {response.status_code}"
    except Exception as e:
        print(f"Error removing webhook: {e}")
        return f"Error removing webhook: Exception: {str(e)}"



tools_config = [
    {
        "type": "function",
        "function": {
            "name": "add_to_webhook",
            "description": "Adds a dynamic route to a Flask app",
            "parameters": {
                "type": "object",
                "properties": {
                    "script_path": {
                        "type": "string",
                        "description": "filename.py #name of the script to be webhooked"
                    },
                    "hook_name": {
                        "type": "string",
                        "description": "give the webhook a cool name"
                    },
                    "hook_description": {
                        "type": "string",
                        "description": "give a description for the hook"
                    }
                },
                "required": ["script_path", "hook_name", "hook_description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "test_webhook",
            "description": "Tests the accessibility of a webhook",
            "parameters": {
                "type": "object",
                "properties": {
                    "webhook_path": {
                        "type": "string",
                        "description": "Full path of the webhook returned by add_to_webhook function, e.g., '/webhook/user_id/random_path'"
                    }
                },
                "required": ["webhook_path"]
            }
        }
    },{
    "type": "function",
    "function": {
        "name": "remove_webhook",
        "description": "Removes a specified webhook for a user",
        "parameters": {
            "type": "object",
            "properties": {
                "path_id": {
                    "type": "string",
                    "description": "Path ID of the webhook to be removed"
                }
            },
            "required": ["path_id"]
        }
    }
},{
        "type": "function",
        "function": {
            "name": "edit_webhook",
            "description": "Edits an existing webhook path for a user",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID associated with the webhook"
                    },
                    "path_id": {
                        "type": "string",
                        "description": "Path ID of the webhook to be edited"
                    },
                    "updates": {
                        "type": "object",
                        "description": "JSON object containing the updates to be made, e.g., {'hook_name': 'New Name', 'hook_description': 'Updated Description'}",
                        "additionalProperties": {
                            "type": "string"
                        }
                    }
                },
                "required": ["user_id", "path_id", "updates"]
            }
        }
    }
]
