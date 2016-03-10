import json

with open('step1.json') as data_file:
    json = json.load(data_file)
    json_ok = [person for person in json.values() if person["condition"] == "OK"]
    print(len(json_ok))
