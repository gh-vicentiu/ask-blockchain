from bitcoinrpc.authproxy import AuthServiceProxy
import time
rpc_user = 'testuser'
rpc_password = 'testpassword'
rpc_host = 'localhost'
rpc_port = 8332
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

# Get the current UNIX timestamp for the start of today
start_of_today = int(time.time()) - (int(time.time()) % 86400)

# Get the list of all transactions since the start of today
transactions = rpc_connection.listsinceblock('', start_of_today)
btc_transacted = sum([abs(tx['amount']) for tx in transactions['transactions']])
print('BTC transacted today:', btc_transacted)