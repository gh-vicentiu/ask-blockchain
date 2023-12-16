import threading
import requests
import uuid

def send_message_to_hook(user_id, messaged_back):
    def do_request():
        url = 'http://localhost:5000/receive_update'
        message_id = str(uuid.uuid4())  # Generate a unique message ID
        data = {
            'user_id': user_id,
            'messaged_back': messaged_back,
            'message_id': message_id  # Include message_id in the data
        }
        try:
            requests.post(url, json=data)
        except requests.exceptions.RequestException as e:
            print(f"Error sending message: {e}")

    threading.Thread(target=do_request).start()
