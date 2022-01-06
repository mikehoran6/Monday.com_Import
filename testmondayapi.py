import requests
import json
from monday import MondayClient

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjEyMjY1NDI2NSwidWlkIjoyMDgyODM5NSwiaWFkIjoiMjAyMS0wOC0zMFQyMDo1ODoxOC42ODdaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6ODQwNTAwMywicmduIjoidXNlMSJ9.ZO2c9M_gmaTIgMCVHIqyFTQq9g5WGSppRtq04nTRHKk"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization" : apiKey}
monday = MondayClient(apiKey)

def test():
    query5 = 'query { users { id name } }' #query team ids
    query2 = 'mutation { create_item (board_id: 1104451842, group_id: "testing", item_name: "SEO SOP") { id } }'
    query3 = 'query { boards (ids:1657373297) { groups {title id} } }'
    query4 = 'query { boards (ids:1510105935) { items { name id } } }'
    query = 'mutation ($parent_item_id: Int!) { create_subitem (parent_item_id:$parent_item_id, item_name: "Fix H1s") { id board { id } } }'
    query = 'mutation { create_group (board_id: 1673060240, group_name: "test group") { id }}'
    query = 'mutation { create_board (board_name: "test", board_kind: public, template_id: 1773458360) { id }}'
    queryclients = 'query { boards (ids:1627574436) { items (limit: 3000) { name id column_values { id value } } } }'
    addlink = 'mutation {change_multiple_column_values(item_id:1764438423, board_id:1510105935, column_values: {\"connect_boards\" : "{\"item_ids\" : [1767405542]}}") {id}}'
    create_item = "mutation { create_item (board_id: 1510105935, group_id: \"new_group70733\", item_name: \"test\", column_values: \"{\\\"connect_boards\\\" : {\\\"item_ids\\\" : [1767405542]}}\") { id } }"
    vars = {'parent_item_id': 1633387063}
    data = {'query': query, 'variables': vars}
    data = {'query': query}
    r = requests.post(url=apiUrl, json=data, headers=headers)
    response = r.json()
    out = open('out.txt', 'w')
    out.write(str(response))
    r = requests.post(url=apiUrl, json=data, headers=headers)
    print()

def addtags():
    query = 'mutation ($board_id: Int!, $item_id: Int!, $columnVals: JSON!) { change_multiple_column_values (item_id:$item_id, board_id:$board_id, column_values:$columnVals) { id } }'
    vars = {
        'board_id': 1627574436,
        'item_id': 1627816601,
        'columnVals': json.dumps({
            'tags': {'tag_ids': [11187115, 10764095]}
        })
    }

    data = {'query': query, 'variables': vars}
    r = requests.post(url=apiUrl, json=data, headers=headers)  # make request
    print(r.json())

def testfield():
    query = 'mutation ($board_id: Int!, $item_id: Int!, $columnVals: JSON!) { change_multiple_column_values (item_id:$item_id, board_id:$board_id, column_values:$columnVals) { id } }'
    vars = {
        'board_id': 1627574436,
        'item_id': 1739486818,
        'columnVals': json.dumps({
            'long_text4': "test\ntest\ntest"
        })
    }

    data = {'query': query, 'variables': vars}
    r = requests.post(url=apiUrl, json=data, headers=headers)  # make request
    print(r.json())

def mondaymodule():
    boards = monday.boards.fetch_boards()
    board = monday.boards.fetch_items_by_board_id(1627574436)
    tags = monday.tags.fetch_tags()
    print()

testfield()