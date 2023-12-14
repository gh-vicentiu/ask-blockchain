from quart import Quart, render_template, request, jsonify, Response, stream_with_context, session, redirect
#from quart import Response, stream_with_context, jsonify
from db import get_mongo_client_async, test_mongo_connection_async
from user_db import register_user_async, check_login_async
import os
import asyncio
import json
import subprocess

app = Quart(__name__)
messages_queue = asyncio.Queue()
secret_key = os.urandom(16)
app.secret_key = secret_key

@app.before_serving
async def before_serving():
    if await test_mongo_connection_async():
        print("Successfully connected to MongoDB.")
    else:
        print("Failed to connect to MongoDB.")

@app.route('/')
async def index():
    if 'username' in session:
        username = session['username']
        client = await get_mongo_client_async()
        db = client['user_database']
        users = db['users']
        user = await users.find_one({"username": username})
        user_id = user.get('user_id', 'Unknown') if user else 'Unknown'
        return await render_template('index.html', username=username, user_id=user_id)
    return redirect('/login')

@app.route('/mongodb')
async def mongodb_page():
    client = await get_mongo_client_async()
    try:
        dbs = await client.list_database_names()
        db_collections = {db_name: await client[db_name].list_collection_names() for db_name in dbs}
        return await render_template('mongodb.html', db_collections=db_collections)
    except Exception as e:
        return str(e)
    finally:
        await client.close()

@app.route('/send_message', methods=['POST'])
async def send_message():
    data = await request.json
    user_id = data.get('user_id', 'default_user_id')
    messaged_us = data.get('messaged_us', 'default_message')
    asyncio.create_task(execute_command(user_id, messaged_us))
    return jsonify({"status": "Command sent"})



@app.route('/stream/<user_id>')
async def stream(user_id):
    async def event_stream(user_id):
        while True:
            message = await messages_queue.get()
            if message['user_id'] == user_id:
                yield f"data: {json.dumps(message)}\n\n"
            await asyncio.sleep(0.1)

    return Response(event_stream(user_id), mimetype="text/event-stream")


@app.route('/receive_update', methods=['POST'])
async def receive_update():
    data = await request.json
    await messages_queue.put(data)
    return jsonify({"status": "Message received"})

async def execute_command(user_id, messaged_us):
    command = ["python3", "main.py", json.dumps({"user_id": user_id, "messaged_us": messaged_us})]
    process = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    async for line in process.stdout:
        print("main.py output:", line.decode('utf-8').strip())
    stderr = await process.communicate()
    if stderr:
        print("STDERR from main.py:", stderr[1].decode('utf-8'))

@app.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        form_data = await request.form
        username = form_data['username']
        password = form_data['password']
        if await check_login_async(username, password):
            session['username'] = username
            return redirect('/')
        else:
            return "Login Failed"
    return await render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
async def signup():
    if request.method == 'POST':
        form_data = await request.form
        username = form_data['username']
        password = form_data['password']
        user_id = await register_user_async(username, password)
        if user_id:
            session['username'] = username
            return redirect('/')
        else:
            return "Signup Failed"
    return await render_template('signup.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
