import time
import openai
import json
import logging
from ai_tools.main_tools import btc_price, blockchain
from ai_tools.secondary_tools import execute_file, create_file
from functions.db_operations import read_db, write_db, r_dbin, w_dbin  # To handle database operations



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
                
                if func_name == "btc_price":
                    output = btc_price(sentTo=arguments['sentTo'], sentFrom=arguments['sentFrom'], instruction=arguments['instruction'], thread_main=thread_main)
                    tool_outputs.append({
                        "tool_call_id": action['id'],
                        "output": output,
                     })
                    
                    if thread_main['agent'] is None:
                        db[user_id][assistant_id][thread_id][message_u_id] = {}
                        db[user_id][assistant_id][thread_id][message_u_id][2] = {"tool":{'instruction': arguments, "timestamp": int(time.time())}}
                   
                    logging.info(f"Agent Sent this: {output}")
                    logging.info(json.dumps(run, default=str, indent=4))

                elif func_name == "blockchain":
                    output = btc_price(sentTo=arguments['sentTo'], sentFrom=arguments['sentFrom'], instruction=arguments['instruction'], thread_main=thread_main)
                    tool_outputs.append({
                        "tool_call_id": action['id'],
                        "output": output,
                     })
                    
                    if thread_main['agent'] is None:
                        db[user_id][assistant_id][thread_id][message_u_id] = {}
                        db[user_id][assistant_id][thread_id][message_u_id][2] = {"tool":{'instruction': arguments, "timestamp": int(time.time())}}
                    
                    logging.info(f"Agent Sent this: {output}")
                    logging.info(json.dumps(run, default=str, indent=4))
                
                elif func_name == "create_file":
                    output = create_file(fileName=arguments['fileName'], fileContent=arguments['fileContent'])
                    tool_outputs.append({
                        "tool_call_id": action['id'],
                        "output": output,
                     })
                    
                    if thread_main['agent'] is None:
                        db[user_id][assistant_id][thread_id][message_u_id] = {}
                        db[user_id][assistant_id][thread_id][message_u_id][2] = {"tool":{'instruction': arguments, "timestamp": int(time.time())}}
                    
                    logging.info(f"Agent Sent this: {output}")
                    logging.info(json.dumps(run, default=str, indent=4))

                elif func_name == "execute_file":
                    output = execute_file(fileName=arguments['fileName'])
                    tool_outputs.append({
                        "tool_call_id": action['id'],
                        "output": output,
                     })
                    
                    if thread_main['agent'] is None:
                        db[user_id][assistant_id][thread_id][message_u_id] = {}
                        db[user_id][assistant_id][thread_id][message_u_id][2] = {"tool":{'instruction': arguments, "timestamp": int(time.time())}}
                    
                    logging.info(f"Agent Sent this: {output}")
                    logging.info(json.dumps(run, default=str, indent=4))

                else:
                    raise ValueError(f"Unknown function: {func_name}")

               
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
