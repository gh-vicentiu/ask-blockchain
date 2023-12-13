from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
rpc_user = 'testuser'
rpc_password = 'testpassword'
rpc_host = 'localhost'
rpc_port = 8332
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

latest_block_hash = rpc_connection.getbestblockhash()
latest_block = rpc_connection.getblock(latest_block_hash)
print('Latest Block:', latest_block)