import logging
import json

def ai_parse_response(messages):
    if messages.data:
        latest_message = messages.data[0]  # Get the first (and only) message in the list

        if latest_message.content and isinstance(latest_message.content, list):
            first_content_item = latest_message.content[0]

            if hasattr(first_content_item, 'text') and hasattr(first_content_item.text, 'value'):
                text_value = first_content_item.text.value
                return text_value  # Return the text content of the latest message
            else:
                logging.error("Content item does not have a 'text' attribute with 'value'.")
        else:
            logging.error("Latest message content is not a list or is empty.")
    else:
        logging.info("No messages found in the thread.")

    return None