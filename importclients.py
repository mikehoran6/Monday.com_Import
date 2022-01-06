import requests
import json
import pandas as pd
from importdomains import importsingledomain, getdomains
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urlparse

#constants
apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjEyMjY1NDI2NSwidWlkIjoyMDgyODM5NSwiaWFkIjoiMjAyMS0wOC0zMFQyMDo1ODoxOC42ODdaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6ODQwNTAwMywicmduIjoidXNlMSJ9.ZO2c9M_gmaTIgMCVHIqyFTQq9g5WGSppRtq04nTRHKk"
apiUrl = "https://api.monday.com/v2"
mondayheaders = {"Authorization": apiKey}
highriseheaders = ('a1d602407f0177f46e739d6db3b60c0d', 'X')
#highrise tag id: monday.com tag id
tagids = {'3511056': '12698418', '6736342': '12698655', '6724500': '12698656', '6725330': '12698661', '6362146': '12335747', '1262049': '12698668', '6671026': '12698672', '6387916': '12698674', '6517709': '12698675', '6491223': '12698679', '6654796': '12698680', '6095864': '12698681', '6516509': '12698682', '6745422': '12698683', '6751286': '12698685', '1410548': '12698687', '6674734': '12335746', '6087272': '10764095', '6096010': '12698693', '4228561': '12698696', '6480900': '12698698', '6743310': '12698699', '1578653': '12698700', '6275932': '12698701'}

def importclient(client_id):
    '''
        importclient imports the highrise client into the Clients board with domains and contacts linked.
        :param client_id: highrise client id
        :param domains: list of associated domains in the monday Domains board
        :param contacts: list of associated contacts in the monday Contacts board
        :return: describe what it returns
    '''
    #get client info from highrise
    client_url = 'https://hozio.highrisehq.com/companies/' + client_id + '.xml'
    rawxml = requests.get(client_url, auth=highriseheaders).text
    xml = BeautifulSoup(rawxml, 'html.parser')

    #sort highrise data into variables
    address_field = ''
    addresses = xml.find('addresses').find_all('address')
    for i in addresses:
        address_field += str(i.street.text) + ', ' + str(i.city.text) + ' ' + str(i.state.text) + ' ' + str(i.zip.text) + '\n'

    email_field = ''
    emails = xml.find('email-addresses').find_all('address')
    for i in emails:
        email_field += i.text + '\n'

    phone_field = ''
    phones = xml.find_all('phone-number')
    for i in phones:
        phone_field += i.number.text + '\n'

    # highrise tag id: monday group id
    groups = {'6725330': 'topics', '1262049': 'new_group16190', '6654796': 'new_group', '6745422': 'new_group23105'}

    tag_ids = []
    tags = xml.find_all('tag')
    group_id = 'topics'
    for i in tags:
        highrise_tag_id = i.id.text
        tag_ids.append(int(tagids[highrise_tag_id]))
        if highrise_tag_id in groups:
            group_id = groups[highrise_tag_id]

    notes_field = ''
    notes = xml.find_all('subject_data')
    for i in notes:
        notes_field += i.find('subject_field_label').text + ': ' + i.find('value').text + '\n'

    created_at = xml.find('created-at').text.split('T')[0]

    # get highrise contacts, import contacts into Contacts board
    contacts = importcontacts(client_id)

    # get highrise domains, import domains into Domains board
    domains = []
    client_domains = getdomains(client_id)
    for domain in client_domains:
        domains.append(int(importsingledomain(domain)))

    # create monday.com API query
    create_item = 'mutation ($board_id: Int!, $group_id: String, $item_name: String, $columnVals: JSON!){ create_item (board_id: $board_id, group_id: $group_id, item_name: $item_name, column_values:$columnVals) { id } }'
    vars = {
        'board_id': 1627574436,
        'group_id': group_id,
        'item_name': xml.find('name').text,
        'columnVals': json.dumps({
            'connect_boards20': {'item_ids': contacts},
            'tags8': {'tag_ids':tag_ids},
            'link_to_domains': {'item_ids': domains},
            'long_text8': notes_field,
            'long_text7': phone_field,
            'long_text74': email_field,
            'long_text4': address_field,
            'date44': {'date': created_at}
        })
    }
    data = {'query': create_item, 'variables': vars}
    response = json.loads(requests.post(url=apiUrl, json=data, headers=mondayheaders).text)
    return int(response['data']['create_item']['id'])

#create client contact on Contact board and note new contact item_id
def importcontacts(client_id):
    contacts = []
    contacts_url = 'https://hozio.highrisehq.com/companies/' + client_id + '/people.xml'
    rawxml = requests.get(contacts_url, auth=highriseheaders).text
    xml = BeautifulSoup(rawxml, 'html.parser')
    people = xml.find_all('person')
    if len(people) == 0:
        return None
    for person in people:
        #get name
        first_name = person.find('first-name').text
        last_name = person.find('last-name').text
        if last_name == '':
            name = first_name
        else:
            name = first_name + ' ' + last_name

        title = person.find('title').text

        phones = person.find_all('phone-number')
        if len(phones) > 0:
            phonetext = ''
            for i in phones:
                text += i.find('number').text + '\n'
        else:
            phonetext = ''

        emails = person.find_all('email-address')
        if len(emails) > 0:
            emailtext = ''
            for i in emails:
                text += i.find('address').text + '\n'
        else:
            emailtext = ''

        #create monday.com API query
        create_item = 'mutation ($board_id: Int!, $group_id: String, $item_name: String, $columnVals: JSON!){ create_item (board_id: $board_id, group_id: $group_id, item_name: $item_name, column_values:$columnVals) { id } }'
        vars = {
            'board_id': 1657373297,
            'group_id': 'topics',
            'item_name': name,
            'columnVals': json.dumps({
                'text0': title,
                'phone3': phonetext,
                'email5': emailtext
            })
        }
        data = {'query': create_item, 'variables': vars}
        response = json.loads(requests.post(url=apiUrl, json=data, headers=mondayheaders).text)
        contacts.append(int(response['data']['create_item']['id']))
    return contacts

def checkdomain(domainsdict, domain):
    return domainsdict


'''
importcontacts('81754055')
importtasks(336377067, "PCG")
importclients({'hozio.com':'1657668892'}, [336377067,336740547])
'''