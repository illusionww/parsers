import re

import unicodecsv as csv

import requests
from bs4 import BeautifulSoup


def getLinksFromPage(pagenum):
    print("perform page", pagenum)
    url = "https://democrator.ru/petition/"
    params = {
        "page": pagenum,
        "per-page": 16,
        "sort": "-created"
    }

    page = requests.get(url, params)
    soup = BeautifulSoup(page.text, "html.parser")
    petition_items = soup.findAll("a", "petition__item-inner")
    return [{"href": petition_item["href"],
             "type": petition_item.find("span", "mark").text
             } for petition_item in petition_items]


def getLinks():
    linksByPage = [getLinksFromPage(i) for i in range(6)]
    l = []
    for linksOfPage in linksByPage:
        l.extend(linksOfPage)
    return l


def parsePage(link):
    print("perform", link["href"])
    url = "https://democrator.ru" + link["href"]
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    text = ""
    paragraphs = soup.find("div", "redactor-editor").findAll("p")
    for paragraph in paragraphs:
        paragraph_text = paragraph.text.replace("\r\n", " ").replace("\n", " ").replace("\r", " ").strip()
        replaced = re.sub(r"[ ]+", " ", paragraph_text)
        text += replaced + "\\n"
    text.strip("\\n")

    petition = {
        'title': soup.find("span", "position-r").text,
        'type': link["type"].strip(),
        'url': url,
        'description': text,
        'vote': soup.find("span", "vote").text.strip(),
        'need_vote': soup.find("span", "need-vote").text.strip(),
        'start_date': soup.findAll("span", "history__item-date")[-1].text.strip()
    }

    return petition

def write(name, initiatives):
    with open(name + ".csv", "wb") as outfile:
        f = csv.writer(outfile, delimiter="^", dialect='excel', encoding='utf-8')

        f.writerow([
            "title",
            "type",
            "url",
            "description",
            "vote",
            "need_vote",
            "start_date"
        ])

        for initiative in initiatives:
            f.writerow([
                initiative["title"],
                initiative["type"],
                initiative["url"],
                initiative["description"],
                initiative["vote"],
                initiative["need_vote"],
                initiative["start_date"]
            ])

def run():
    links = getLinks()
    petitions = [parsePage(link) for link in links]
    write("democrator", petitions)

run()
