#filename ai-make/create_ai.py - keep this comment always
import openai
import json
import logging

client = openai.Client()


def create_assistant(agent=None):
    from ai_tools.main_tools import tools_list
    from ai_tools.secondary_tools import tools_lite
    from ai_tools.route_tools import tools_route
    tool_list = tools_list
    tool_lite = tools_lite
    tool_route = tools_route

    if agent == "relay":
        assistant = client.beta.assistants.create(
        name=agent,
        #instructions=("you are a relay node. use [btc_price] function to ask 'btc_price' any questions regarding bitcoin price. use [ask_blockchain] function to ask 'ask_blockchain' any questions regarding bitcoin price."),
        instructions=("You are the manager of a team that develops and deploys webhooks. You and your team are specialized into building webhooks for blockchain querries.. \n\n"
                      "You will be approach by more or less savy customers that will ask of you things you might not be able to do or do.\n"
                      "If the client is vague or uncertain you will have a discusion with them before building the webhook to inquire of them about what they want from this webhook to do.\n"
                      "Under your command there are 2 agents:\n"
                      "'agent_coder': he can code scripts that query the bitcoin blockchain.\n\n"
                      "'agent_webhook': he can setup the webhook once the query script is functional.\n"
                      "To be able to build a webhook for the clients, you will have to instruct and coordonate the company agents under you.\n"
                      "The procedure is this:\n"
                      "1. You will make sure the client requirement is clear\n"
                      "2. You will give 'agent_coder' all the details about the query and you will inquire of him the name of the working scripts\n"
                      "3. You will give 'agent_webhook' the name of the script agent coder created and instruct him to setup the webhook.\n"
                      ),
        tools=tool_list,
        model="gpt-3.5-turbo-1106"        
    )
    elif agent == "agent_webhook":
        assistant = client.beta.assistants.create(
        name=agent,
        instructions=("You are in charge of setting up webhooks, you will be given the scripts filename that needs to be executed when the route is called.\n"
                    "use the function calling tools at your disposal to setup the route.\n"
                      ),
        tools=tool_route,
        model="gpt-3.5-turbo-1106"        
    )
    elif agent == "agent_coder":
        assistant = client.beta.assistants.create(
        name=agent,
        instructions=("You are a code generator specialized in creating Python scripts for querying a Bitcoin full node blockchain using the bitcoinrpc.authproxy library. \n\n"
                      "When provided with a user's question your task is to interpret the question and generate the appropriate Python code snippet that can be executed to retrieve the query from a fully synced local Bitcoin node.\n\n"
                      "The code should be complete, including necessary imports, and should handle typical query types for specific dates or ranges that cover the entire chain if necessary. \n\n"
                      "To do so, you can use the [create_file] and [execute_file] functions.\n\n"
                      "at the end return the filename and path\n\n"
                      "#python - start here\n"
                      "from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException\n"
                      "rpc_user = 'testuser'\n"
                      "rpc_password = 'testpassword'\n"
                      "rpc_host = '62.231.64.203'\n"
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
