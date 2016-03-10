import html
from datetime import datetime

import requests
import unicodecsv as csv

base = "https://www.roi.ru/api/"


def getInitiative(id):
    print("try to get initiative with id", id)
    initiative = requests.get(base + "petition/" + str(id) + ".json").json()["data"]
    # if len(initiative["decision"]) > 1:
    #     print("HELP I NEED SOMEBODY")
    return initiative


def normalizeText(text):
    return html.unescape(text).replace("<br />", "").replace("\r\n", "\\n")

def normalizeDate(date):
    return datetime.fromtimestamp(int(date))

def write(name, initiatives):
    with open(name + ".csv", "wb") as outfile:
        f = csv.writer(outfile, delimiter="^", dialect='excel', encoding='utf-8')

        f.writerow([
            "id",
            "code",
            "url",
            "title",
            "description",
            "decision",
            "prospective",
            "level.title",
            "category.title"
            "status.title",
            "result.title",
            "date.poll.begin",
            "date.poll.end",
            "vote.progress",
            "vote.threshold",
            "vote.affirmative",
            "vote.negative"
        ])

        for initiative in initiatives:
            f.writerow([
                initiative["id"],
                initiative["code"],
                initiative["url"],
                normalizeText(initiative["title"]),
                normalizeText(initiative["description"]),
                "\n".join([normalizeText(decision["text"]) for decision in initiative["decision"]]) if "decision" in initiative else "",
                normalizeText(initiative["prospective"]),
                initiative["level"]["title"],
                "\n".join([category["title"] for category in initiative["category"]]) if "category" in initiative else "",
                initiative["status"]["title"],
                initiative["result"]["title"] if "result" in initiative else "",
                normalizeDate(initiative["date"]["poll"]["begin"]),
                normalizeDate(initiative["date"]["poll"]["end"]),
                str(initiative["vote"]["progress"]).replace(".", ","),
                initiative["vote"]["threshold"],
                initiative["vote"]["affirmative"],
                initiative["vote"]["negative"],
            ])

def run(name):
    print("RUN", name)
    poll = requests.get(base + "petitions/" + name + ".json").json()["data"]
    initiatives = [getInitiative(init["id"]) for init in poll]
    write("all_" + name, initiatives)

run("poll")
run("advisement")
run("complete")
run("archive")
