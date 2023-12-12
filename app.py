import requests
import threading
import subprocess
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import json
import queue
import time
from functions.return_response import send_message_to_hook


app = Flask(__name__)
messages_queue = queue.Queue()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_id = data.get('user_id', 'default_user_id')
    messaged_us = data.get('messaged_us', 'default_message')
    # Start execute_command in a new thread
    thread = threading.Thread(target=execute_command, args=(user_id, messaged_us,))
    thread.start()
    return jsonify({"status": "Command sent"})

@app.route('/stream/<user_id>')
def stream(user_id):
    def event_stream(user_id):
        while True:
            try:
                message = messages_queue.get()  # Blocking get, waits for a message
                if message['user_id'] == user_id:
                    yield f"data: {json.dumps(message)}\n\n"
            except queue.Empty:
                pass
            time.sleep(0.1)
    return Response(stream_with_context(event_stream(user_id)), mimetype="text/event-stream")

@app.route('/receive_update', methods=['POST'])
def receive_update():
    data = request.json
    messages_queue.put(data)
    return jsonify({"status": "Message received"})

def execute_command(user_id, messaged_us):
    # Running main.py in a subprocess
    command = ["python3", "main.py", json.dumps({"user_id": user_id, "messaged_us": messaged_us})]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Optionally, read the output line by line for debugging (not sending it via send_message_to_hook)
    for line in process.stdout:
        print("main.py output:", line.decode('utf-8').strip())

    # Check for errors
    stderr = process.communicate()[1]
    if stderr:
        print("STDERR from main.py:", stderr.decode('utf-8'))





if __name__ == '__main__':
    app.run(debug=True, threaded=True)
