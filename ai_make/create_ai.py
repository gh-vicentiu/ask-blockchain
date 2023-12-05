#filename ai-make/create_ai.py - keep this comment always
import openai
import json
import logging

client = openai.Client()


def create_assistant(agent=None):
    from ai_tools.main_tools import tools_list
    from ai_tools.secondary_tools import tools_lite
    tool_list = tools_list
    tool_lite = tools_lite

    if agent == "relay":
        assistant = client.beta.assistants.create(
        name=agent,
        #instructions=("you are a relay node. use [btc_price] function to ask 'btc_price' any questions regarding bitcoin price. use [ask_blockchain] function to ask 'ask_blockchain' any questions regarding bitcoin price."),
        instructions=("You are a sales agent for bitcoin. If you are asked any information about blockchain. you will will send a proper formulated request, send to 'blockchain' use [blockchain] function"),

        tools=tool_list,
        model="gpt-3.5-turbo-1106"        
    )
    elif agent == "btc_price":
        assistant = client.beta.assistants.create(
        name=agent,
        instructions=("you are a bitcoin price master. make up prices as you are asked"),
        model="gpt-3.5-turbo-1106"        
    )
    elif agent == "blockchain":
        assistant = client.beta.assistants.create(
        name=agent,
        instructions=("you are a bitcoin blockchain coder, you will be sent requests and your job is to transform them into executable python code, you will save them to file and then execute them."),
        tools=tools_lite,
        model="gpt-3.5-turbo-1106"        
    )
    else:
        logging.info(agent)
        raise ValueError("Invalid agent specified")

    return assistant


if __name__ == "__main__":
    assistant = create_assistant()
    print(f"Assistant created: {assistant}")
