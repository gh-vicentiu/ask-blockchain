from bitcoinrpc.authproxy import AuthServiceProxy
rpc_user = 'testuser'
rpc_password = 'testpassword'
rpc_host = 'localhost'
rpc_port = 8332
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

# Get the latest block info
latest_block_hash = rpc_connection.getbestblockhash()
latest_block = rpc_connection.getblock(latest_block_hash)
block_size = latest_block['size']
print(block_size)