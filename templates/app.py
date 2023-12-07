from flask import Flask, render_template, request, jsonify
import subprocess
import json
import threading
import queue
import  time

app = Flask(__name__)

# Queue to store messages from external POST requests
messages_queue = queue.Queue()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_id = data['user_id']
    message = data['message']

    # Execute the command in a new thread
    thread = threading.Thread(target=execute_command, args=(user_id, message,))
    thread.start()

    return jsonify({"status": "Command sent"})

def execute_command(user_id, message):
    command = f"python3 main.py '{{\"user_id\": \"{user_id}\", \"messaged_us\": \"{message}\"}}'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Debugging: Print the output and error (if any) from main.py
    print(f"STDOUT from main.py: {stdout.decode('utf-8')}")
    if stderr:
        print(f"STDERR from main.py: {stderr.decode('utf-8')}")

@app.route('/receive_update', methods=['POST'])
def receive_update():
    data = request.json
    user_id = data['user_id']
    message = data['message']
    message_id = time.time()  # Use current timestamp as a unique identifier

    # Add the message along with its identifier to the queue
    messages_queue.put((message_id, user_id, message))
    print(f"Received update: {data}, ID: {message_id}")  # Debug print
    return jsonify({"status": "Message received"})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages = []
    while not messages_queue.empty():
        message = messages_queue.get()
        print(f"Sending message: {message}")  # Debug print
        messages.append(message)
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True)
