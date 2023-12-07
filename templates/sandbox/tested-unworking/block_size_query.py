from bitcoinrpc.authproxy import AuthServiceProxy
rpc_user = 'testuser'
rpc_password = 'testpassword'
rpc_host = 'localhost'
rpc_port = 8332
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

latest_block_info = rpc_connection.getblock(rpc_connection.getbestblockhash())
latest_block_size = latest_block_info['size']
print('Latest block size:', latest_block_size)