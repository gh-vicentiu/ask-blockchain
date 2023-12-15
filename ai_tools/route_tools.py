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
    }
]
