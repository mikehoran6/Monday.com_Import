import requests
import json
import pandas as pd
from importdomains import importsingledomain, importdomains, getdomains
from importclients import importclient
from importtasks import importtasks
from importnotes import importnotes

#todo: TQDM
#TODO: CREATE MONDAY ACCOUNTS, CHANGE NAMES IN highriseauthors FOR MONDAY PERSON IDs

def main():
    #make list of client highrise IDs
    client_highrise_ids = []
    client_file = open('clients.txt', 'r')
    for line in client_file:
        client_highrise_ids.append(line.rstrip('\n'))

    #for every client
    for client_id in client_highrise_ids:
        client_item_id = importclient(client_id)
        importnotes(client_id, client_item_id)
        importtasks(client_id,client_item_id)

main()