from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_user = 'username'
rpc_password = 'password'
rpc_ip = '127.0.0.1'
rpc_port = '8332'

rpc_connection = AuthServiceProxy(f'http://{rpc_user}:{rpc_password}@{rpc_ip}:{rpc_port}')

def get_transaction_count():
    try:
        transaction_count = rpc_connection.gettransactioncount()
        print(f'Total transactions in wallet: {transaction_count}')
    except JSONRPCException as e:
        print(f'Error: {e}')

get_transaction_count()
