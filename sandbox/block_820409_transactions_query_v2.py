from bitcoinrpc.authproxy import AuthServiceProxy
rpc_user = 'testuser'
rpc_password = 'testpassword'
rpc_host = 'localhost'
rpc_port = 8332
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

block_820409_hash = rpc_connection.getblockhash(820409)
block_820409 = rpc_connection.getblock(block_820409_hash)
block_820409_transactions = block_820409['tx']
print('List of transactions from block 820409:')
for txid in block_820409_transactions:
    print(txid)