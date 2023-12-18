import requests
import json
import random
import string

def make_http_request(method, url, data=None, headers=None):
    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "GET":
            response = requests.get(url, headers=headers)
        else:
            return "Unsupported HTTP method"

        if response.ok:
            return response.json()
        else:
            return f"HTTP {method} request failed with status code: {response.status_code}"
    except Exception as e:
        return f"Error during HTTP {method} request: {str(e)}"


def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def add_to_webhook(script_path, hook_name, hook_description, user_id):
    data = {
        "user_id": user_id, 
        "path": generate_random_string(), 
        "script_path": f'sandbox/{user_id}/{script_path}', 
        "hook_name": hook_name, 
        "hook_description": hook_description
    }
    response = make_http_request("POST", "http://127.0.0.1:5000/dohook/", data)
    return response

def test_webhook(webhook_path):
    response = make_http_request("GET", f"http://127.0.0.1:5000/{webhook_path}")
    return response

def remove_webhook(path_id, user_id):
    url = f"http://127.0.0.1:5000/remove_user_paths/{user_id}/{path_id}"
    response = make_http_request("POST", url)
    return response

def edit_webhook(path_id, updates, user_id):
    url = f"http://127.0.0.1:5000/edit_user_path/{user_id}/{path_id}"
    response = make_http_request("POST", url, updates)
    return response



tools_route = [
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
