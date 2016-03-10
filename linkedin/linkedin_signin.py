import requests
from bs4 import BeautifulSoup

from constants.linkedin_urls import LinkedinUrls


def signin(session):
    root_page = session.get(LinkedinUrls.root)
    soup = BeautifulSoup(root_page.text, "html.parser")
    join_linkedin_form = soup.find("form", "join-linkedin-form")


    params = {
        "firstName": firstName,
        "lastName": lastName,
        "emailAddress": emailAddress,
        "password": password,
        "isJsEnabled": "true",
        "trcode": "reg-cold-signup-home",
        "regCsrf": join_linkedin_form("input", name="regCsrf"),
        "referer": "",
        "source": "",
        "referrerPageKey": "reg-cold-signup-home",
        "csrfToken": join_linkedin_form("input", name="csrfToken")
    }
    session.post(LinkedinUrls.join_submit_url, data=params)


if __name__ == "__main__":
    session = requests.Session()
    signin(session)
