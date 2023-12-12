import requests
import threading
import subprocess
import json
import queue
import time
import uuid
from functions.return_response import send_message_to_hook
from functions.db_operations import w_udbin, r_udbin
from flask import Flask, render_template, request, jsonify, Response, stream_with_context, session, redirect

app = Flask(__name__)
messages_queue = queue.Queue()
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        users = r_udbin()
        user_id = users.get(username, {}).get('user_id', 'Unknown')
        return render_template('index.html', user_id=user_id)
    return redirect('/login')


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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_login(username, password):
            session['username'] = username
            return redirect('/')
        else:
            return "Login Failed"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = register_user(username, password)
        if user_id:
            session['username'] = username
            return redirect('/')
        else:
            return "Signup Failed"
    return render_template('signup.html')


def generate_user_id():
    return f"{uuid.uuid4().hex[:4]}_{uuid.uuid4().hex[:4]}"

def register_user(username, password):
    users = r_udbin()
    if username in users:
        return False  # User already exists
    user_id = generate_user_id()
    users[username] = {"password": password, "user_id": user_id}
    w_udbin(users)
    return user_id

def check_login(username, password):
    users = r_udbin()
    return users.get(username, {}).get('password') == password



if __name__ == '__main__':
    app.run(debug=True, threaded=True)
