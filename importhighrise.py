import requests
import json
import pandas as pd
from importdomains import importsingledomain, importdomains, getdomains
from importclients import importcontacts
from importnotes import importnotes

def main():
    #make list of client highrise IDs
    client_highrise_ids = []
    client_file = open('clients.txt', 'r')
    for line in client_file:
        client_highrise_ids.append(line.rstrip('\n'))

    #for every client
    for client_id in client_highrise_ids:

        #get associated domains, import domains into Domains board
        #domainsdict : list of monday Domains board item ids
        client_domains = getdomains(client_id)
        domain_item_ids = []
        for domain in client_domains:
            domain_item_ids.append(importsingledomain(domain))

        #get associated contacts, import contacts into Contacts board
        #contacts : list of monday Contacts board item ids
        contact_item_ids = importcontacts(client_id)

        #import client
        #import tasks
        #import notes

main()