from New import client, BASE_URL, API_KEY
import requests


def fetch_districts(states: list):
    _states = requests.get(BASE_URL+'/metadata/states', headers={
        'Api-key': API_KEY}).json()["states"]

    districts = []
    for state in states:
        for s in _states:
            if s['state_name'] == state:
                _districts = requests.get(
                    BASE_URL + f'/metadata/districts/{s["state_id"]}', headers={'API-Key': API_KEY}).json()['districts']
                districts_list = [x['district_name'] for x in _districts]
                districts.extend(districts_list)
    return districts
