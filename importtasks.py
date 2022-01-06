import requests
import json
from bs4 import BeautifulSoup

#TODO: CREATE MONDAY ACCOUNTS, CHANGE NAMES IN highriseauthors FOR MONDAY PERSON IDs

#constants
apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjEyMjY1NDI2NSwidWlkIjoyMDgyODM5NSwiaWFkIjoiMjAyMS0wOC0zMFQyMDo1ODoxOC42ODdaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6ODQwNTAwMywicmduIjoidXNlMSJ9.ZO2c9M_gmaTIgMCVHIqyFTQq9g5WGSppRtq04nTRHKk"
apiUrl = "https://api.monday.com/v2"
mondayheaders = {"Authorization": apiKey}
highriseheaders = ('a1d602407f0177f46e739d6db3b60c0d', 'X')
#highrise author id : monday.com user id
highriseauthors = {'1428939':'Rita Orza', '1421544':'Amit Singh', '1271729':'Clynton Minott', '1408759':20828395, '1421543':'David Townsend', '1434531':'Erick Romero', '1431552':'Frank Cap', '1020077':'John Bosco', '1434532':'Joseph Puente', '1271728':'Matt Ross', '1428670':'Matthew Zolciak', '1435400':'Michael Little', '1020269':'20828395', '279715':'Steven Orandello', '1434530':'Tyler Rodriguez', '1428533':'Vincent Nicolo'}


def importtasks(client_id, client_item_id):
    #get all tasks for client
    tasks_url = 'https://hozio.highrisehq.com/companies/' + client_id + '/tasks.xml'
    rawxml = requests.get(tasks_url, auth=highriseheaders).text
    xml = BeautifulSoup(rawxml, 'html.parser')
    tasks = xml.find_all('task')
    if len(tasks) == 0:
        return None
    for task in tasks:
        #get date
        due_date = task.find('due-at').text.split("T")[0]
        task_body = task.find('body').text
        author = task.find('owner-id').text

        # create monday.com API query
        create_subitem = 'mutation ($parent_item_id: Int, $item_name: String, $columnVals: JSON!){ create_subitem (parent_item_id: $parent_item_id, item_name: $item_name, column_values:$columnVals) { id board { id } } }'
        vars = {
            'parent_item_id': client_item_id,
            'item_name': task_body,
            'columnVals': json.dumps({
                'long_text': task_body,
                'date0': due_date,
                'person': {'personsAndTeams': [{'id': highriseauthors[author], 'kind': 'person'}]},
                'status': {'label': "HIGH"}
            })
        }
        data = {'query': create_subitem, 'variables': vars}
        response = json.loads(requests.post(url=apiUrl, json=data, headers=mondayheaders).text)
    return None