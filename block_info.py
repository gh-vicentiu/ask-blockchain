import requests

url = 'https://blockchain.info/latestblock'
response = requests.get(url)
block_info = response.json()
print(block_info)