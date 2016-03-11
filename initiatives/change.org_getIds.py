import requests
from bs4 import BeautifulSoup


def getInitiativeIdsFromPage(pagenum):
    print("page", pagenum)
    url = "https://www.change.org/ru/%D0%BF%D0%B5%D1%82%D0%B8%D1%86%D0%B8%D0%B8?hash=most-recent&hash_prefix=most-recent&list_type=default&view=most-recent&page=" + str(
        pagenum)
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "referer": "https://www.change.org/petitions",
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
        'x-csrf-token': 'd64fe7386b18813a51727a2eab8bae45',
        'x-requested-with': 'XMLHttpRequest'
    }
    page = requests.get(url, headers=headers)
    json = page.json()
    soup = BeautifulSoup(json["html"], "html.parser")
    petitions = soup.findAll("li", "petition")
    return [petition["data-id"] for petition in petitions]


def aggregateIds():
    idsByPage = [getInitiativeIdsFromPage(i) for i in range(1, 745)]
    all_ids = []
    for idsInPage in idsByPage:
        all_ids.extend(idsInPage)
    return all_ids


def first_step():
    ids = aggregateIds()
    with open('change.org_ids.txt', "w") as f:
        for item in ids:
            f.write("%s\n" % item)


first_step()
