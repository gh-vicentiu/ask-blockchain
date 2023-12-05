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
        instructions=("You are an intention relay hub, your task is to understand what the user wants and pass properly formulated istructions to one of the 2 agents under you. sendTo 'agent_btc' by using [call_agent_btc] function to find out bitcoin related things. You sendTo 'agent_coder' by using [call_agent_coder] any coding related tasks"),

        tools=tool_list,
        model="gpt-3.5-turbo-1106"        
    )
    elif agent == "agent_btc":
        assistant = client.beta.assistants.create(
        name=agent,
        instructions=("you are a bitcoin price master. make up prices as you are asked"),
        model="gpt-3.5-turbo-1106"        
    )
    elif agent == "agent_coder":
        assistant = client.beta.assistants.create(
        name=agent,
        instructions=("you are a proffesional coder. you will transform incoming requests into a py script that you will execute. To do so, you can use [create_file] and [execute_file] functions"),
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
