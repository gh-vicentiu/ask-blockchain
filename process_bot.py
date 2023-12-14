import asyncio
import json
import logging
import openai
from ai_make.create_ai import create_assistant
from ai_make.create_thread import create_thread
from ai_run.send_mess import add_message_to_thread
from ai_run.run_ai import run_assistant
from functions.db_operations import read_db_async, write_db_async
from functions.ai_parse_response import ai_parse_response
from functions.return_response import send_message_to_hook_async

client = openai.Client(api_key='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')

async def process_bot(instruction, thread_main):
    logging.info(f"Processing bot {thread_main['agent']}: {thread_main['u_bot_0_id']} with message: {instruction}")

    db = await read_db_async()

    ids = 'a'
    assistant_id = db[thread_main['u_bot_0_id']][ids].get(thread_main['agent'] + '_assistant_id')
    if not assistant_id:
        logging.info(f"Creating new assistant for {thread_main['agent']}.")
        assistant = create_assistant(thread_main['agent'])
        assistant_id = assistant.id
        db[thread_main['u_bot_0_id']][ids][thread_main['agent'] + "_assistant_id"] = assistant_id
        await write_db_async(db)

    thread_id = db[thread_main['u_bot_0_id']][ids].get(thread_main['agent'] + '_thread_id')
    if not thread_id:
        logging.info(f"Creating new thread for {thread_main['agent']}.")
        thread_id = create_thread()
        db[thread_main['u_bot_0_id']][ids][thread_main['agent'] + '_thread_id'] = thread_id
        db[thread_main['u_bot_0_id']][assistant_id][thread_id] = {}
        await write_db_async(db)

    message_u_id = add_message_to_thread(thread_id, instruction, role='user', agent=thread_main['agent'])
    logging.info(f"Message {message_u_id} added to {assistant_id} - {thread_id} for {thread_main['u_bot_0_id']}.")
    if message_u_id not in db[thread_main['u_bot_0_id']][assistant_id][thread_id]:
        db[thread_main['u_bot_0_id']][assistant_id][thread_id][message_u_id] = {}
    db[thread_main['u_bot_0_id']][assistant_id][thread_id][message_u_id]['0'] = {"sent": {"role": "user", "content": instruction}}
    await write_db_async(db)

    thread_main_updated = {
        'a_bot_1_id': assistant_id, 't_bot_1_id': thread_id, 'm_bot_1_id': message_u_id,
        'agent': thread_main['agent'], 'u_bot_0_id': thread_main['u_bot_0_id'],
        'a_bot_0_id': thread_main['a_bot_0_id'], 't_bot_0_id': thread_main['t_bot_0_id'],
        'm_bot_0_id': thread_main['m_bot_0_id']
    }
    thread_full = await run_assistant(thread_main_updated)
    ai_replay = ai_parse_response(thread_full)
    await send_message_to_hook_async(thread_main['u_bot_0_id'], ai_replay)
    db[thread_main['u_bot_0_id']][assistant_id][thread_id][message_u_id]['1'] = {"replay": {"role": "assistant", "content": ai_replay}}
    await write_db_async(db)

    return ai_replay

# This block allows the script to be run as a standalone Python script for testing
if __name__ == "__main__":
    import sys

    user_id = sys.argv[1]
    instruction = json.loads(sys.argv[2])['message']

    asyncio.run(process_bot(instruction, {
        'agent': 'some_agent',
        'u_bot_0_id': user_id,
        'a_bot_0_id': 'some_assistant_id',
        't_bot_0_id': 'some_thread_id',
        'm_bot_0_id': 'some_message_id'
    }))
