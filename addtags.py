import requests

highriseheaders = ('e5aab53af28867da4ff53484b783d2a0', 'X')
headers = {'Content-Type': 'application/xml'}
client_id = str(333995336)

req_url = 'https://hozio.highrisehq.com/companies/' + client_id + '/tags.xml'

data = '<name>Test</name>'
test = requests.post(req_url, data=data, headers=headers, auth=highriseheaders)

print()

