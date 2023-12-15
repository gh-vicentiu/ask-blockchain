from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
rpc_user = 'testuser'
rpc_password = 'testpassword'
rpc_host = '62.231.64.203'
rpc_port = 8332
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

def get_latest_blocks(count):
    try:
        latest_blocks = []
        block_number = rpc_connection.getblockcount()
        for i in range(count):
            block_hash = rpc_connection.getblockhash(block_number - i)
            block = rpc_connection.getblock(block_hash)
            latest_blocks.append((block_number - i, block_hash, block))
        return latest_blocks
    except JSONRPCException as e:
        return f'Error: {e}'

latest_10_blocks = get_latest_blocks(10)
for block_info in latest_10_blocks:
    block_number, block_hash, block = block_info
    print(f"Block Number: {block_number}, Block Hash: {block_hash}")