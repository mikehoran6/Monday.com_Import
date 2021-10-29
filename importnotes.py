import requests
import json
from bs4 import BeautifulSoup

#constants
apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjEyMjY1NDI2NSwidWlkIjoyMDgyODM5NSwiaWFkIjoiMjAyMS0wOC0zMFQyMDo1ODoxOC42ODdaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6ODQwNTAwMywicmduIjoidXNlMSJ9.ZO2c9M_gmaTIgMCVHIqyFTQq9g5WGSppRtq04nTRHKk"
apiUrl = "https://api.monday.com/v2"
mondayheaders = {"Authorization": apiKey}
highriseheaders = ('a1d602407f0177f46e739d6db3b60c0d', 'X')
highriseauthors = {'1428939':'Mike Horan', '1421544':'Amit Singh', '1271729':'Clynton Minott', '1408759':'Damian Lester', '1421543':'David Townsend', '1434531':'Erick Romero', '1431552':'Frank Cap', '1020077':'John Bosco', '1434532':'Joseph Puente', '1271728':'Matt Ross', '1428670':'Matthew Zolciak', '1435400':'Michael Little', '1020269':'Rita Orza', '279715':'Steven Orandello', '1434530':'Tyler Rodriguez', '1428533':'Vincent Nicolo'}

#Import all highrise notes by Highrise client ID
def importnotes():
    #query list of clients from Clients Board and return list as clients
    queryclients = 'query { boards (ids:1627574436) { items (limit: 3000) { name id column_values (ids: "text0") { value } } } }'
    data = {'query': queryclients}
    r = requests.post(url=apiUrl, json=data, headers=mondayheaders)
    response = r.json()
    clients = response['data']['boards'][0]['items']

    #go through all clients and import updates from highrise, import tags and client information
    for client in clients:
        notes = gethighrisenotes(client['column_values'][0]['value'].strip('"'))
        #note_id: update_id
        updates = {}
        for note in notes:
            if 'parent_id' in note:
                comment_body = highriseauthors[note['author']] + '\n' + note['body'] + '\n' + note['created']
                create_comment = 'mutation { create_update (item_id: ' + client['id'] + ', parent_id: ' + updates[note['parent_id']] + ' body: "' + comment_body + '") { id } }'
                data = {'query': create_comment}
                requests.post(url=apiUrl, json=data, headers=mondayheaders)
                continue
            update_body = highriseauthors[note['author']] + '\n' + note['body'] + '\n' + note['created']
            create_update = 'mutation { create_update (item_id: ' + client['id'] + ', body: "' + update_body + '") { id } }'
            data = {'query': create_update}
            response = json.loads(requests.post(url=apiUrl, json=data, headers=mondayheaders).text)
            updates[note['note_id']] = response['data']['create_update']['id']

#Get all notes for client by client ID using highrise xml structure, check if each has any comments, and return list of notes/comments(dicts)
def gethighrisenotes(client_id):
    n = 0
    all_notes = []
    while True:
        page = n * 25
        company_url = 'https://hozio.highrisehq.com/companies/' + client_id + '/notes.xml?n=' + str(page)
        rawxml = requests.get(company_url, auth=highriseheaders).text
        xml = BeautifulSoup(rawxml, 'html.parser')
        notes = xml.find_all('note')
        if len(notes) == 0:
            break
        for note in notes:
            all_notes.extend(comments(note.find('id').text))
            all_notes.insert(0, {'author': note.find('author-id').text, 'body': note.find('body').text, 'created': note.find('created-at').text.split('T')[0], 'note_id': note.find('id').text})
        n += 1
    return all_notes

#get all comments assosciated with a note by note ID using highrise xml structure and associate with the parent note
def comments(note_id):
    all_comments = []
    note_url = 'https://hozio.highrisehq.com/notes/' + note_id + '/comments.xml'
    rawxml = requests.get(note_url, auth=highriseheaders).text
    xml = BeautifulSoup(rawxml, 'html.parser')
    comments = xml.find_all('comment')
    for comment in comments:
        all_comments.insert(0, {'author': comment.find('author-id').text, 'body': comment.find('body').text, 'created': comment.find('created-at').text.split('T')[0], 'parent_id': note_id})
    return all_comments

