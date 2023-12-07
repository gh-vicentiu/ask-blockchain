import requests

def send_message_to_hook(user_id, message):
    url = 'http://localhost:5000/receive_update'  # Adjust the URL if necessary
    data = {
        'user_id': user_id,
        'message': message
    }
    try:
        response = requests.post(url, json=data)
        return response.json()  # Or just response.status_code if you don't need the response body
    except requests.exceptions.RequestException as e:
        # Handle any errors here (e.g., connection error)
        print(f"Error sending message: {e}")

