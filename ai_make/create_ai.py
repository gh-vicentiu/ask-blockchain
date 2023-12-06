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
        instructions=("Your a PR Agent, your task is to answer bitcoin related questions, and bitcoin related questions only. Any questions regarding btc price you will submit to agent_price and any questions that require blockchain full node intergotiations you will pass to agent_coder. Else, you can answer yourself."),

        tools=tool_list,
        model="gpt-3.5-turbo-1106"        
    )
    elif agent == "agent_price":
        assistant = client.beta.assistants.create(
        name=agent,
        instructions=("you are a bitcoin price master. make up prices as you are asked"),
        model="gpt-3.5-turbo-1106"        
    )
    elif agent == "agent_coder":
        assistant = client.beta.assistants.create(
        name=agent,
        instructions=("You are a code generator specialized in creating Python scripts for querying a local Bitcoin node blockchain using the bitcoinrpc.authproxy library. \n\n"
                      "When provided with a user's question your task is to interpret the question and generate the appropriate Python code snippet that can be executed to retrieve the query from a fully synced local Bitcoin node.\n\n"
                      "The code should be complete, including necessary imports, and should handle typical query types for specific dates or ranges that cover the entire chain if necessary. \n\n"
                      "To do so, you can use the [create_file] and [execute_file] functions.\n\n"
                      "#python - start here\n"
                      "from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException\n"
                      "rpc_user = 'testuser'\n"
                      "rpc_password = 'testpassword'\n"
                      "rpc_host = 'localhost'\n"
                      "rpc_port = 8332\n"
                      "rpc_connection = AuthServiceProxy(f\"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}\")\n"
                      "#rest of the script:\n"
                      "[create_file]\n"
                      "Your task is to generate the Python script to answer the following user question:\n\n"
                      "[execute_file]\n"
                      ),
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
