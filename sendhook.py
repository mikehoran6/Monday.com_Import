import requests
import json

webhook_url = "http://192.168.1.124:8080/createtasksgroup"
headers = {
    'Content-Type': 'application/json'
}

data = {'challenge': '3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P'}

r = requests.post(webhook_url, data=json.dumps(data), headers=headers)

print()