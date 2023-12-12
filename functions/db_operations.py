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

def w_udbin(data):
    try:
        with open('usdb.json', 'w') as file:
            json.dump(data, file, indent=8)
        print("Database updated. w_dbin")
    except Exception as e:
        print(f"Error updating database w_dbin: {e}")

def r_udbin():
    try:
        with open('usdb.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("usdb.json not found, creating a new one.")
        return {}
    
    return message_id