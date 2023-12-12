import threading
import requests

def send_message_to_hook(user_id, messaged_back):
    def do_request():
        url = 'http://localhost:5000/receive_update'
        data = {
            'user_id': user_id,
            'messaged_back': messaged_back
        }
        try:
            requests.post(url, json=data)
        except requests.exceptions.RequestException as e:
            print(f"Error sending message: {e}")

    # Run the request in a background thread
    threading.Thread(target=do_request).start()
