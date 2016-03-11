import re

import requests
import unicodecsv as csv

params = {
    "api_key": "b88aa9bd2ded773d238aa851cb1c210fb48a9a74b7ed2fbd69db322b7ab13c2e"
}

def getInitiatives(ids):
    params["petition_ids"] = ids
    json = requests.get("https://api.change.org/v1/petitions/", params=params).json()
    return json["petitions"]

def write(name, initiatives):
    with open(name + ".csv", "wb") as outfile:
        f = csv.writer(outfile, delimiter="^", dialect='excel', encoding='utf-8')

        f.writerow([
            "petition_id",
            "url",
            "title",
            "overview",
            "category",
            "status",
            "created_at",
            "end_at",
            "signature_count",
            "goal",
            "targets"
        ])

        for initiative in initiatives:
            overview = initiative["overview"]
            overview = re.sub("<.+?>", "", overview).replace("\r\n", "\\n").replace("\n", "\\n").replace("\r", "\\n").strip()

            f.writerow([
                initiative["petition_id"],
                initiative["url"],
                initiative["title"].replace("\r\n", " ").replace("\n", " ").replace("\r", " ").strip(),
                overview,
                initiative["category"],
                initiative["status"],
                initiative["created_at"],
                initiative["end_at"],
                initiative["signature_count"],
                initiative["goal"],
                "\\n".join([target["name"] for target in initiative["targets"]])
            ])

def run():
    with open("change.org_ids.txt", "r") as f:
        ids = f.read().splitlines()
        chunks = [",".join(ids[x:x+500]) for x in range(0, len(ids), 500)]
    all_petitions = []
    for chunk in chunks:
        pet = getInitiatives(chunk)
        all_petitions.extend(pet)
    write("change.org_petitions", all_petitions)

run()