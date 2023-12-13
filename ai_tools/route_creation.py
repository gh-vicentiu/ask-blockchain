from flask import jsonify
from .secondary_tools import execute_file
import json

# Generic route handler function
def create_route_handler(file_path):
    def handler():
        output = execute_file(file_path)
        return jsonify({"output": output})
    return handler

def load_dynamic_routes(app):
    try:
        with open('routes_config.json', 'r') as file:
            config = json.load(file)
            for route in config['routes']:
                add_dynamic_route(app, route['path'], route['file_path'])
    except FileNotFoundError:
        print("routes_config.json not found. No dynamic routes loaded.")
    except json.JSONDecodeError:
        print("Error decoding routes_config.json. Check the file format.")


def add_dynamic_route(app, route, file_path):
    if not route.startswith('/'):
        route = '/' + route
    handler = create_route_handler(file_path)
    app.add_url_rule(route, endpoint=route, view_func=handler, methods=['GET'])

    with open('routes_config.json', 'r') as file:
        config = json.load(file)

    # Add new route
    config['routes'].append({"path": route, "file_path": file_path})

    # Save updated config
    with open('routes_config.json', 'w') as file:
        json.dump(config, file, indent=4)



tools_route = [
    {
        "type": "function",
        "function": {
            "name": "add_dynamic_route",
            "description": "Adds a dynamic route to a Flask app",
            "parameters": {
                "type": "object",
                "properties": {
                    "app": {
                        "type": "object",
                        "description": "The Flask app instance to which the route will be added"
                    },
                    "route": {
                        "type": "string",
                        "description": "The URL rule as a string"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "The file path associated with the route"
                    }
                },
                "required": ["route", "file_path"]
            }
        }
    }
]

