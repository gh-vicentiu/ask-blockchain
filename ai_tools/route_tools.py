import requests
import json
import random
import string

def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def add_to_webhook(script_path, thread_main):
    url = "http://127.0.0.1:5000/dohook/"
    headers = {"Content-Type": "application/json"}
    user_id = thread_main['u_bot_0_id']
    
    # Generate a random 8-character string for url_path
    url_path = generate_random_string()
    
    data = {"path": url_path, "script_path": 'sandbox/' + user_id + '/' + script_path}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("success"):
            print(f"Path '{url_path}' added successfully with script path '{script_path}'")
            return (f"(success: /webhook/{url_path})")
        else:
            print("Error adding data:", response_data.get("error"))
            return "Error"
    else:
        print("HTTP POST request failed with status code:", response.status_code)
        return response.status_code

tools_route = [
    {
        "type": "function",
        "function": {
            "name": "add_to_webhook",
            "description": "Adds a dynamic route to a Flask app",
            "parameters": {
                "type": "string",
                "properties": {
                    "script_path": {
                        "type": "string",
                        "description": "filename.py #name of the script to be webhooked"
                    }
                },
                "required": ["script_path"]
            }
        }
    }
]
