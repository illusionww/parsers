import requests
from bs4 import BeautifulSoup

with open("change.org_urls.txt", "r") as f:
    urls = f.read().splitlines()

forknum = 7

titles = []
for url in urls[1000*forknum:1000*forknum + 1000]:
    print("process", url)
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")
    title = soup.find("h1", "mbxs").text
    title = title.replace("\r\n", " ").replace("\n", " ").replace("\r", " ").strip()
    titles.append(title)

with open("change.org_titles"+ str(forknum) + ".txt", "w", encoding="utf-8") as f:
    for item in titles:
        f.write("%s\n" % item)