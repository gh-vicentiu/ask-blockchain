# main.py
import sys
import json
import process_user
import logging
#from functions.db_operations import read_db_chats, write_db_chats # To handle database operations

# Read the current state of the database
#db = read_db_chats(user_id)


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
