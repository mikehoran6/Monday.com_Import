import requests
import json
import pandas as pd
from importdomains import importsingledomain, importdomains
from importclients import importclients
from importnotes import importnotes

def main():
    # domain : item_id
    domains = {}
    domains.update(importdomains('649.csv', "649"))
    print()


main()