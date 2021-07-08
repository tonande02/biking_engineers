import json
import requests


# my Frost client_id (Tonje)
client_id = "6d199937-3f7a-48cb-9c12-384cecb6cb07"

# the url - filtering on county=Oslo
endpoint = "https://frost.met.no/sources/v0.jsonld?types=SensorSystem&county=Oslo*"


# returns the full data as python dict
def fetch_data_from_frost(url, client_id):
    r = requests.get(endpoint, auth=(client_id,''))

    # checking that the request went ok
    assert r.ok
    assert r.status_code == 200

    data = r.json() # entire raw content
    return data

# returns just info on the stations in a dict
def filter_stations_from_data(data):
    stations = data["data"]

    return stations

# prints info on stations to terminal in a readable manner
def view_stations(data):
    station_nr = 1
    for station in data:
        print(f"Station nr: {station_nr}")
        print(station["name"])
        print(station["shortName"])
        print(station["id"])
        print(f"Coordinates: {station['geometry']['coordinates']}")
        station_nr += 1
        print()

# writes the data to filepath as a json-file
def write_data_to_file(data, filepath):
    with open(filepath, "w") as file:
        json.dump(data, file, indent=2)



# get the data
data = fetch_data_from_frost(endpoint, client_id)
stations = filter_stations_from_data(data)

# # ---- run this to write the data to file ----
# path = "test_frost.json" # add correct path here
# write_data_to_file(data, path)


# # ---- run this to view content in terminal --
# # view relevant info on each station
# view_stations(stations)
# # view whole data file in formatted json style
# pretty_data = json.dumps(data, indent=2)
# print(pretty_data)
