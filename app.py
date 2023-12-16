import json
import subprocess
import threading
import queue
import time
import uuid
import os
from flask import Flask, render_template, request, jsonify, Response, stream_with_context, session, redirect
from db import get_mongo_client, test_mongo_connection
from user_db import register_user, check_login
from functions.db_operations import load_from_db, save_to_db, get_user_paths, remove_user_paths, edit_user_path

app = Flask(__name__)
messages_queue = queue.Queue()
secret_key = os.urandom(16)
app.secret_key = secret_key
user_paths = load_from_db()
message_acknowledgments = {}



def generate_unique_message_id():
    return str(uuid.uuid4())

def send_message_to_queue(user_id, messaged_us):
    message_id = generate_unique_message_id()
    message = {"user_id": user_id, "messaged_back": messaged_us, "message_id": message_id}
    messages_queue.put(message)
    message_acknowledgments[message_id] = {"message": message, "acknowledged": False, "timestamp": time.time()}

def message_resender():
    while True:
        for message_id, message_info in list(message_acknowledgments.items()):
            if not message_info['acknowledged'] and time.time() - message_info['timestamp'] > 10:
                print(f"Resending message {message_id}")
                messages_queue.put(message_info['message'])
                message_info['timestamp'] = time.time()
        time.sleep(5)

threading.Thread(target=message_resender, daemon=True).start()

@app.route('/acknowledge_message', methods=['POST'])
def acknowledge_message():
    data = request.json
    message_id = data.get('message_id')
    if message_id in message_acknowledgments:
        message_acknowledgments[message_id]['acknowledged'] = True
        return jsonify({"status": "Acknowledgment received"})
    return jsonify({"status": "Message ID not found"})

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        client = get_mongo_client()
        db = client['user_database']
        users = db['users']
        user = users.find_one({"username": username})
        user_id = user.get('_id', 'Unknown') if user else 'Unknown'
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

    # Execute main.py with user_id and messaged_us
    execute_command(user_id, messaged_us)

    # No need to send this message to the SSE queue
    return jsonify({"status": "Message sent and processed"})

@app.route('/stream/<user_id>')
def stream(user_id):
    def event_stream(user_id):
        try:
            yield 'data: {"type": "connection_established"}\n\n'
            while True:
                message = messages_queue.get()
                if message['user_id'] == user_id:
                    yield f"data: {json.dumps(message)}\n\n"
                time.sleep(0.2)
        except Exception as e:
            app.logger.error(f"Stream error: {e}")
    return Response(stream_with_context(event_stream(user_id)), mimetype="text/event-stream")

@app.route('/receive_update', methods=['POST'])
def receive_update():
    data = request.json
    message_id = data.get('message_id')
    if message_id:
        message_acknowledgments[message_id] = {"message": data, "acknowledged": False, "timestamp": time.time()}
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


@app.route('/get_user_paths/<user_id>')
def user_paths(user_id):
    paths = get_user_paths(user_id)
    return jsonify(paths)

@app.route('/remove_user_paths/<user_id>/<path_id>', methods=['POST'])
def remove_path(user_id, path_id):
    # Logic to remove path from the database
    success = remove_user_paths(user_id, path_id)
    return jsonify({"success": success})

@app.route('/edit_user_path/<user_id>/<path_id>', methods=['POST'])
def edit_path(user_id, path_id):
    if request.is_json:
        updates = request.get_json()
        # Call the edit_user_path function with the provided data
        success = edit_user_path(user_id, path_id, updates)
        if success:
            return jsonify({"success": True, "message": "Path updated successfully."})
        else:
            return jsonify({"success": False, "message": "Failed to update the path."})
    else:
        return jsonify({"success": False, "error": "Invalid data, JSON expected."})


@app.route('/dohook/', methods=['POST'])
def webhook():
    user_paths = load_from_db()  # Load the latest data from MongoDB

    if request.is_json:
        data = request.get_json()
        user_id = data.get('user_id')
        path = data.get('path')
        hook_info = {
            "script_path": data.get('script_path'),
            "hook_name": data.get('hook_name'),
            "hook_description": data.get('hook_description')
        }

        if user_id and path and hook_info["script_path"]:
            if user_id not in user_paths:
                user_paths[user_id] = {}
            user_paths[user_id][path] = hook_info
            save_to_db(user_paths)  # Save to MongoDB
            
            # Generate a unique message ID
            message_id = generate_unique_message_id()
            
            # Create message data
            message_data = {
                "user_id": user_id,
                "type": "new_path",
                "path_info": {
                    "id": path,
                    "url": f"/webhook/{user_id}/{path}",
                    "name": hook_info.get("hook_name"),
                    "description": hook_info.get("hook_description"),
                    "exists": os.path.exists(hook_info.get("script_path"))
                },
                "message_id": message_id  # Include the message ID
            }

            # Send SSE message for new path
            messages_queue.put(message_data)

            # Add to message acknowledgments
            message_acknowledgments[message_id] = {"message": message_data, "acknowledged": False, "timestamp": time.time()}

            return jsonify({"success": True, "user_id": user_id, "path": path, "hook_info": hook_info})

    return jsonify({"success": False, "error": "Invalid data"})


@app.route('/webhook/<user_id>/<path:path>')
def custom_path(user_id, path):
    user_paths = load_from_db()  # Fetch fresh data from MongoDB

    if user_id in user_paths and path in user_paths[user_id]:
        path_info = user_paths[user_id][path]
        if isinstance(path_info, dict) and 'script_path' in path_info:
            script_path = path_info['script_path']
            try:
                output = subprocess.check_output(['python3', script_path], stderr=subprocess.STDOUT, text=True)
                return jsonify({"output": output})
            except subprocess.CalledProcessError as e:
                return jsonify({"error": f"Error executing script for path {path}: {e.output}"})
        else:
            return jsonify({"error": f"Path information for {path} is incorrect"})
    else:
        return jsonify({"error": "User ID or Path not found"})

#start

if __name__ == '__main__':
    if test_mongo_connection():
        print("Successfully connected to MongoDB.")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Failed to connect to MongoDB.")
