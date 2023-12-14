import asyncio
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

async def process_user_async(user_id, messaged_us):
    logging.info(f"Processing user: {user_id} with message: {messaged_us}")

    db = await read_db_async()

    if user_id not in db:
        logging.info(f"User {user_id} NOT found, creating a new entry.")
        db[user_id] = {}
        await write_db_async(db)

    assistant_id = db[user_id].get('last_assistant_id')
    if not assistant_id:
        assistant = create_assistant("relay")
        assistant_id = assistant.id
        db[user_id]['last_assistant_id'] = assistant_id
        db[user_id][assistant_id] = {}  # Initialize sub-dictionary
        await write_db_async(db)

    thread_id = db[user_id].get('last_thread_id')
    if not thread_id:
        thread_id = create_thread()
        db[user_id]['last_thread_id'] = thread_id
        db[user_id][assistant_id][thread_id] = {}  # Initialize sub-sub-dictionary
        await write_db_async(db)

    if assistant_id not in db[user_id]:
        db[user_id][assistant_id] = {}

    if thread_id not in db[user_id][assistant_id]:
        db[user_id][assistant_id][thread_id] = {}

    message_u_id = add_message_to_thread(thread_id, messaged_us, role='user')
    db[user_id][assistant_id][thread_id][message_u_id] = {"sent": {"role": "user", "content": messaged_us}}
    await write_db_async(db)

    thread_main = {'u_bot_0_id': user_id, 'a_bot_0_id': assistant_id, 't_bot_0_id': thread_id, 'm_bot_0_id': message_u_id, 'agent': None}
    thread_full = await run_assistant(thread_main)
    ai_reply = ai_parse_response(thread_full)

    await send_message_to_hook_async(user_id, ai_reply)

    db[user_id][assistant_id][thread_id][message_u_id]['reply'] = {"role": "assistant", "content": ai_reply}
    await write_db_async(db)

    return ai_reply
