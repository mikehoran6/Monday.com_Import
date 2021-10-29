import requests
import json
import pandas as pd
from importdomains import importsingledomain
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urlparse

#constants
apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjEyMjY1NDI2NSwidWlkIjoyMDgyODM5NSwiaWFkIjoiMjAyMS0wOC0zMFQyMDo1ODoxOC42ODdaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6ODQwNTAwMywicmduIjoidXNlMSJ9.ZO2c9M_gmaTIgMCVHIqyFTQq9g5WGSppRtq04nTRHKk"
apiUrl = "https://api.monday.com/v2"
mondayheaders = {"Authorization": apiKey}
highriseheaders = ('a1d602407f0177f46e739d6db3b60c0d', 'X')
#highrise author id : monday.com user id
highriseauthors = {'1428939':'20828395', '1421544':'Amit Singh', '1271729':'Clynton Minott', '1408759':'Damian Lester', '1421543':'David Townsend', '1434531':'Erick Romero', '1431552':'Frank Cap', '1020077':'John Bosco', '1434532':'Joseph Puente', '1271728':'Matt Ross', '1428670':'Matthew Zolciak', '1435400':'Michael Little', '1020269':'20828395', '279715':'Steven Orandello', '1434530':'Tyler Rodriguez', '1428533':'Vincent Nicolo'}

#highrise ID : [contact item_id]
contacts = defaultdict(list)

#check for domain, if not created in Domains sheet, create it
#create client contact on Contact board and note new contact item_id
#create client item on Clients board and link contact and domain
def importclients(domainsdict, clients):
    for client in clients:
        #get client info from highrise
        client_url = 'https://hozio.highrisehq.com/companies/' + str(client) + '.xml'
        rawxml = requests.get(client_url, auth=highriseheaders).text
        xml = BeautifulSoup(rawxml, 'html.parser')
        company = xml.find('company')
        contact_data = company.find('contact-data')
        websites = contact_data.find_all('web-adderess')

        #import associated contacts and return item IDs from Contacts Board
        contacts = importcontacts(client)
        #create client task group and create any tasks for client in group on Client Tasks Board
        importtasks(client, client_name)

        #check all websites and import to domains sheet if not already
        for site in websites:
            domainsdict = checkdomain(domainsdict, site.find('url').text)

def importcontacts(client):
    contacts = []
    contacts_url = 'https://hozio.highrisehq.com/companies/' + str(client) + '/people.xml'
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

        #create monday.com API query
        create_item = 'mutation ($board_id: Int!, $group_id: String, $item_name: String){ create_item (board_id: $board_id, group_id: $group_id, item_name: $item_name) { id } }'
        vars = {
            'board_id': 1657373297,
            'group_id': 'topics',
            'item_name': name,
            'columnVals': json.dumps({
                'text0': person.find('title').text
            })
        }
        data = {'query': create_item, 'variables': vars}
        response = json.loads(requests.post(url=apiUrl, json=data, headers=mondayheaders).text)
        contacts.append(response['data']['create_item']['id'])
    return contacts

def importtasks(client, client_name):
    #create task group in Client Tasks Board
    #query = 'mutation { create_board (board_name: "test", board_kind: public, template_id: 1773458360) { id }}'
    create_group = "mutation { create_group (board_id: 1673060240, group_name: \"" + client_name + "\") { id }}"
    data = {'query': create_group}
    response = json.loads(requests.post(url=apiUrl, json=data, headers=mondayheaders).text)
    group_id = response['data']['create_group']['id']

    #get all tasks for client
    tasks_url = 'https://hozio.highrisehq.com/companies/' + str(client) + '/tasks.xml'
    rawxml = requests.get(tasks_url, auth=highriseheaders).text
    xml = BeautifulSoup(rawxml, 'html.parser')
    tasks = xml.find_all('task')
    if len(tasks) == 0:
        return None
    for task in tasks:
        #get date
        alert_date = task.find('alert-at').text.split("T")[0]
        task_body = task.find('body').text
        author = task.find('author-id').text

        # create monday.com API query
        create_task = "mutation ($board_id: Int!, $group_id: String, $item_name: String){ create_item (board_id: $board_id, group_id: $group_id, item_name: $item_name, column_values: \"{\\\"date\\\" : {\\\"date\\\" : \\\"" + alert_date + "\\\"}, \\\"person\\\" : {\\\"personsAndTeams\\\":[{\\\"id\\\":" + highriseauthors[author] + ",\\\"kind\\\":\\\"person\\\"}]}}\") { id } }"
        vars = {
            'board_id': 1673060240,
            'group_id': group_id,
            'item_name': task_body
        }
        data = {'query': create_task, 'variables': vars}
        response = json.loads(requests.post(url=apiUrl, json=data, headers=mondayheaders).text)
    return None

def checkdomain(domainsdict, domain):
    return domainsdict


importtasks(336377067, "PCG")
importclients({'hozio.com':'1657668892'}, [336377067,336740547])