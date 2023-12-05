#filename setup/create_thread.py - keep this comment always
import openai  # Make sure to import openai

client = openai.Client()  # Initialize the OpenAI client

def create_thread():
    # Make an API call to create a thread and return the thread ID
    thread_response = client.beta.threads.create()  # Adjust this line according to the actual API method
    return thread_response.id  # Assuming the response has an 'id' attribute
