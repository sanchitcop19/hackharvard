# This is written for PYTHON 3
# Don't forget to install requests package

import requests
import json

customerId = '5dab1ecc322fa016762f32ba'
apiKey = '9a9b28bee3b788f897c76ceca369b6da'

url = f'http://api.reimaginebanking.com/customers/{customerId}/accounts?key={apiKey}'
payload = {
  "type": "Credit Card",
  "nickname": "test",
  "rewards": 10000,
  "balance": 10000,
}
# Create a Savings Account
response = requests.post(
	url,
	data=json.dumps(payload),
	headers={'content-type':'application/json'},
	)

if response.status_code == 201:
	print('account created')
