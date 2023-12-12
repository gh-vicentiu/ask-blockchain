from bitcoinrpc.authproxy import AuthServiceProxy
rpc_user = 'testuser'
rpc_password = 'testpassword'
rpc_host = 'localhost'
rpc_port = 8332
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

latest_block_hash = rpc_connection.getbestblockhash()
latest_block = rpc_connection.getblock(latest_block_hash)
block_txids = latest_block['tx']
total_btc_transacted = 0.0
for txid in block_txids:
    transaction = rpc_connection.getrawtransaction(txid, True)
    for details in transaction['details']:
        if details['category'] == 'send':
            total_btc_transacted += details['amount']
print('Total BTC transacted in the latest block:', total_btc_transacted)