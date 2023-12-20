# ask-blockchain
LLM Python based application that allows users to ask normal natural language questions to a bitcoin validator node and get valid answers.

This project is brought by https://www.edoar.ai. Let's get you an edoar [do]!

Ask blockchain takes advantage of the new open ai assistents, running throu api locally, using them to write code on the fly 
in order to provide it's user with answers to blockchain alatitics mysteries. 

The app is designed around one main agent who has pretrained knowledge about the opperation, 
that has under him a series of specialized ai agents who it can summon them and delacated to more specific tasks
like either coding for blockchain or coding for price history analytics.

This is not a swarm type design aldo it will implement swarm type based tools in order to find answers tomore difficult questions.


This is BETA! version

REQUIREMENTS:

ENV openai api
export OPENAI_API_KEY=

ENV mongoDB uri
export MONGODB_URI=""

0.  how you start it?
    python3 app.py    
    go to: http://localhost:5000

1. what it is?
    ask blockchain is an app that allows users to interogate the blockchain for deep analytics,
    and it will setup an api endpoint where the updated information can be retrieved. 
    also historic price related questions will be added very soon, as of now.


2. how it works?
    user sends a command via the web interface    
    eg: make me a hook to get the latest block count
    with the magic of AI a spell is casted and and an api end point is created 
    with constants updates about this information

3. how it really works?
    user sends a question to an AI agent,
    the agent will answer the question or pass it to another specialized agent
    that agent will write and execute the code
    if the code works the information will be passed to another agent that will setup the API end point.
    the answer returns to the first agent and relayed back to the user.


!!! OPEN AI KEY REQUIRED !!! 

    20 december first beta version
    it's alive and talks back!
    Since alpha
    Ui implemented
    MongoDb implemented
    the system now designs webhooks as well
    better error handleing
    improved and expanded code
    huge update!

What to expect. for now...
    5 dececmber 2023
    first alpha version!

    the main coder for blockchain is not yet active, we are in testing stages.
    
    The main agent will talk to you, 
    01.    if you require of him the price of btc, it will call another agent that will make up a price and gives it back
    02.    if you require of him to code for you, it will write py code save it in /sandbox/ and it will execute it

    it is quite buggy yet, but works for the most part.

    to be added:
        better error handeling
        blockchain coder assistant
        code debugger

