# Import the bitcoinrpc library
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Set up the connection to the local Bitcoin node
rpc_user = 'testuser'
rpc_password = 'testpassword'
rpc_host = 'localhost'
rpc_port = 8332
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

# Count to 1
for i in range(1, 2):
    print(i)