import openai
import logging
import json


client = openai.Client()

def add_message_to_thread(thread_id, messaged_us, role='user'):
    try:
        logging.info(f"Adding Message to thread: {messaged_us}")
        added_message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,
            content=messaged_us
        )

        # Log the message ID and its details
        logging.info(f"Message ID registered: {added_message.id}")
        logging.info(json.dumps(added_message, default=str, indent=4))

        return added_message.id

    except Exception as e:
        logging.error(f"Error in add_message_to_thread: {e}")
        # Removed the incorrect logging line referencing 'run'
        return None
