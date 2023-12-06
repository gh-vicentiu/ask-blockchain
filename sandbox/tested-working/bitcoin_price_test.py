import requests

url = 'http://127.0.0.1:5000/bitcoin-price'
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print('Current Bitcoin Price in USD:', data['price_in_usd'])
else:
    print('Failed to fetch Bitcoin price')