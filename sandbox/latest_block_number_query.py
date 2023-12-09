from bitcoinrpc.authproxy import AuthServiceProxy
rpc_user = 'testuser'
rpc_password = 'testpassword'
rpc_host = 'localhost'
rpc_port = 8332
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

latest_block_number = rpc_connection.getblockcount()
print('Latest block number:', latest_block_number)