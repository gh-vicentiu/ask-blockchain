import asyncio
import openai
import json
import logging
from ai_tools.main_tools import call_agent_price, call_agent_coder
from ai_tools.secondary_tools import execute_file, create_file, move_files
from ai_tools.tool_calls import (handle_call_agent_price, handle_call_agent_coder,
                                 handle_create_file, handle_execute_file, handle_move_files)
from functions.db_operations import read_db_async, write_db_async
from functions.return_response import send_message_to_hook_async

client = openai.Client()

async def run_assistant(thread_main):
    db = await read_db_async()  # Async read from DB

    if thread_main['agent'] is None:
        logging.info("Starting the main assistant...")
        thread_id = thread_main['t_bot_0_id']
        assistant_id = thread_main['a_bot_0_id']
        message_u_id = thread_main['m_bot_0_id']
    else:
        logging.info("Starting the secondary bots...")
        thread_id = thread_main['t_bot_1_id']
        assistant_id = thread_main['a_bot_1_id']
        message_u_id = thread_main['m_bot_1_id']
    user_id = thread_main['u_bot_0_id']

    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id, instructions="")
    logging.info("Assistant run initiated.")

    while True:
        logging.info("Checking run status...")
        await asyncio.sleep(3)

        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        if run_status.status == 'completed':
            logging.info("Run completed. Fetching messages...")
            messages = client.beta.threads.messages.list(thread_id=thread_id, limit=1, order='desc')
            logging.info(f"Messages fetched from the thread {messages}.")
            return messages

        elif run_status.status == 'requires_action':
            logging.info("Function calling...")
            required_actions = run_status.required_action.submit_tool_outputs.model_dump()
            tool_outputs = []

            for action in required_actions["tool_calls"]:
                func_name = action['function']['name']
                arguments = json.loads(action['function']['arguments'])
                action_id = action['id']

                await send_message_to_hook_async(user_id, messaged_back=f"{thread_main['agent']}, '{func_name}'")

                handlers = {
                    "call_agent_price": handle_call_agent_price,
                    "call_agent_coder": handle_call_agent_coder,
                    "create_file": handle_create_file,
                    "execute_file": handle_execute_file,
                    "move_files": handle_move_files
                }

                db_entry = {}
                if func_name in handlers:
                    await handlers[func_name](arguments, thread_main, tool_outputs, db_entry, action_id)
                    await send_message_to_hook_async(user_id, messaged_back=str(tool_outputs))

                if thread_main['agent'] is None and db_entry:
                    db[user_id][assistant_id][thread_id][message_u_id] = db_entry
                    await write_db_async(db)

            if tool_outputs:
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
            else:
                logging.error("No tool outputs to submit.")

        elif run_status.status == 'failed':
            logging.error("Run failed. Exiting...")
            if run_status.last_error:
                error_message = run_status.last_error.message if run_status.last_error.message else 'Unknown error'
                logging.error(f"Error details: {error_message}")
            return None

        else:
            logging.info("Waiting for the Assistant to process...")
            await asyncio.sleep(3)

    return None

# Set up basic logging
logging.basicConfig(level=logging.INFO, filename='assistant_run.log',
                    format='%(asctime)s:%(levelname)s:%(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))
logging.getLogger().addHandler(console_handler)

# Example usage of run_assistant in an async context
# async def main():
#     thread_main = {"agent": None, "t_bot_0_id": "some_id", ...}  # Populate with actual data
#     await run_assistant(thread_main)

# asyncio.run(main())
