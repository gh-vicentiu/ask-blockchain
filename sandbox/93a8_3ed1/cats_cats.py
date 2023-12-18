from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
rpc_user = 'testuser'
rpc_password = 'testpassword'
rpc_host = '62.231.64.203'
rpc_port = 8332
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

# Query the blockchain
print('cats are nice')