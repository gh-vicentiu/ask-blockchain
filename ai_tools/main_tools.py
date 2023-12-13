#filename ai_tools/main_tools.py - keep this comment always
import json


def call_agent_webhook(sentTo, sentFrom, instruction, thread_main):
    from process_bot import process_bot
    print(f"Sending message from {sentFrom} to {sentTo}: '{instruction}'")
    thread_main['agent'] = sentTo
    response = process_bot(instruction=instruction, thread_main=thread_main)
    return f"result {response}"

def call_agent_coder(sentTo, sentFrom, instruction, thread_main):
    from process_bot import process_bot
    print(f"Sending message from {sentFrom} to {sentTo}: '{instruction}'")
    thread_main['agent'] = sentTo
    response = process_bot(instruction=instruction, thread_main=thread_main)
    return f"result {response}"

tools_list = [{
    "type": "function",
    "function": {
        "name": "call_agent_webhook",
        "description": "send messages using this function",
        "parameters": {
            "type": "object",
            "properties": {
                "sentTo": {
                    "type": "string",
                    "description": "message for"
                },
                "sentFrom": {
                    "type": "string",
                    "description": "message from"
                },
                "instruction": {
                    "type": "string",
                    "description": "you call agent webhook in order to create dynamic routes"
                }
            },
            "required": ["sentTo", "sentFrom", "instruction"]
        }
    }
}, {
    "type": "function",
    "function": {
        "name": "call_agent_coder",
        "description": "send messages using another function",
        "parameters": {
            "type": "object",
            "properties": {
                "sentTo": {
                    "type": "string",
                    "description": "message for"
                },
                "sentFrom": {
                    "type": "string",
                    "description": "message from"
                },
                "instruction": {
                    "type": "string",
                    "description": "ask your question to another_function here"
                }
            },
            "required": ["sentTo", "sentFrom", "instruction"]
        }
    }
}]