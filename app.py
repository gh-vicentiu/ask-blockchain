import requests
import threading
import subprocess
import json
import queue
import time
from flask import Flask, render_template, request, jsonify, Response, stream_with_context, session, redirect
from db import get_mongo_client, test_mongo_connection
from user_db import register_user, check_login
import os

app = Flask(__name__)
messages_queue = queue.Queue()
secret_key = os.urandom(16)
app.secret_key = secret_key

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']

        # Get the MongoDB client and fetch the user's details
        client = get_mongo_client()
        db = client['user_database']  # Use your actual database name
        users = db['users']  # Use your actual collection name

        user = users.find_one({"username": username})
        if user:
            user_id = user.get('user_id', 'Unknown')
        else:
            user_id = 'Unknown'

        return render_template('index.html', username=username, user_id=user_id)
    return redirect('/login')

@app.route('/mongodb')
def mongodb_page():
    client = get_mongo_client()
    try:
        dbs = client.list_database_names()
        db_collections = {db_name: client[db_name].list_collection_names() for db_name in dbs}
        return render_template('mongodb.html', db_collections=db_collections)
    except Exception as e:
        return str(e)
    finally:
        client.close()

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

    # Optionally, read the output line by line for debugging
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

# Additional routes can be added here

if __name__ == '__main__':
    if test_mongo_connection():
        print("Successfully connected to MongoDB.")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Failed to connect to MongoDB.")
