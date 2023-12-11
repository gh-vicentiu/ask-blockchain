import time
import openai
import json
import logging
from ai_tools.main_tools import call_agent_price, call_agent_coder
from ai_tools.secondary_tools import execute_file, create_file, move_files
from ai_tools.tool_calls import handle_call_agent_price, handle_call_agent_coder, handle_create_file, handle_execute_file, handle_move_files
from functions.db_operations import read_db, write_db, r_dbin, w_dbin  # To handle database operations
from functions.return_response import send_message_to_hook



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
                action_id = action['id']  # Extract the action ID

                # Refactored: Using a dictionary to map function names to handler functions
                handlers = {
                    "call_agent_price": handle_call_agent_price,
                    "call_agent_coder": handle_call_agent_coder,
                    "create_file": handle_create_file,
                    "execute_file": handle_execute_file,
                    "move_files": handle_move_files
                }

                db_entry = {}  # Initialize an empty dictionary for database entry
                if func_name in handlers:
                    handlers[func_name](arguments, thread_main, tool_outputs, db_entry, action_id)
                try:
                    result = send_message_to_hook(user_id, message=(func_name, tool_outputs))
                    if result is not None:
                        print("Message sent successfully:", result)
                    else:
                        print("Failed to send the message.")
                except Exception as e:
                    print(f"An error occurred: {e}")
                else:
                    logging.error(f"Unknown function: {func_name}")

                # Update the database if needed
                if thread_main['agent'] is None and db_entry:
                    db[user_id][assistant_id][thread_id][message_u_id] = db_entry
                    write_db(db)

               
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