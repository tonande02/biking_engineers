import requests
import pprint
import json

client_id = "abd5c534-9699-4349-b4e0-5bb937752eaa"

endpoint = "https://frost.met.no/observations/v0.jsonld"

parameters = {
    'sources': 'SN18700,SN90450',
    'elements': 'mean(air_temperature PT1H),sum(precipitation_amount PT1H)',
    'referencetime': '2021-06-01T00:00:00.000Z/2021-07-01T00:00:00.000Z',
}

r = requests.get(endpoint, parameters, auth=(client_id,''))

print(r.ok)
print(r.status_code)

json = r.json()
len(json)
json["data"]
