import requests
import json
import pandas as pd
from collections import defaultdict

# constants
apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjEyMjY1NDI2NSwidWlkIjoyMDgyODM5NSwiaWFkIjoiMjAyMS0wOC0zMFQyMDo1ODoxOC42ODdaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6ODQwNTAwMywicmduIjoidXNlMSJ9.ZO2c9M_gmaTIgMCVHIqyFTQq9g5WGSppRtq04nTRHKk"
apiUrl = "https://api.monday.com/v2"
mondayheaders = {"Authorization": apiKey}
#server# : group_id
servers = {"649": "new_group70733", "609": "new_group30273", "544": "new_group359", "493": "new_group30273", "479": "new_group6883"}

def importdomains(file, server):
    df = pd.read_csv(file)
    # domain : item_id
    domains = {}

    # import all domains to Domains board
    for i in df.index:
        IP = df.loc[i, 'IP']
        domain = df.loc[i, 'Domain']
        if isnan(domain):
            continue
        create_item = 'mutation ($board_id: Int!, $group_id: String, $item_name: String){ create_item (board_id: $board_id, group_id: $group_id, item_name: $item_name) { id } }'
        vars = {
            'board_id': 1657668859,
            'group_id': 'topics',
            'item_name': str(domain)
        }
        data = {'query': create_item, 'variables': vars}
        r = requests.post(url=apiUrl, json=data, headers=mondayheaders)
        domains[domain] = json.loads(r.text)['data']['create_item']['id']

    #link all domains to each unique IP on the All IPs board
    unique_ips = df["IP"].unique()
    for unique_ip in unique_ips:
        domainlist = df.loc[df['IP'] == unique_ip]['Domain'].tolist()
        if isnan(domainlist[0]):
            addtoallips(unique_ip, None, server)
            continue
        for index in range(len(domainlist)):
            domainlist[index] = int(domains[domainlist[index]])
        addtoallips(unique_ip, domainlist, server)
    return domains

#Add unique IP to All IPs board and link new item to all associated domains
def addtoallips(unique_ip, domainslist, server):
    if domainslist == None:
        create_item = "mutation { create_item (board_id: 1510105935, group_id: \"" + servers[server] + "\", item_name: \"" + unique_ip + "\") { id } }"
        data = {'query': create_item}
    else:
        create_item = "mutation { create_item (board_id: 1510105935, group_id: \"" + servers[server] + "\", item_name: \"" + unique_ip + "\", column_values: \"{\\\"connect_boards\\\" : {\\\"item_ids\\\" : " + str(domainslist) + "}}\") { id } }"
        data = {'query': create_item}
    requests.post(url=apiUrl, json=data, headers=mondayheaders)

#import domain to Domains board and return the new item id
def importsingledomain(domain):
    create_item = 'mutation ($board_id: Int!, $group_id: String, $item_name: String){ create_item (board_id: $board_id, group_id: $group_id, item_name: $item_name) { id } }'
    vars = {
        'board_id': 1657668859,
        'group_id': 'topics',
        'item_name': str(domain)
    }
    data = {'query': create_item, 'variables': vars}
    r = requests.post(url=apiUrl, json=data, headers=mondayheaders)
    return json.loads(r.text)['data']['create_item']['id']

def isnan(value):
    return value != value

