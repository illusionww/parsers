import json
from datetime import datetime

from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession


class Statistics:
    def __init__(self):
        super().__init__()


class LinkedinSearchParser:
    root_url = 'https://www.linkedin.com'
    login_submit_url = 'https://www.linkedin.com/uas/login-submit'
    search_url = 'https://www.linkedin.com/vsearch/pj'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
    login_static_data = {
        # 'session_key': 'vladimir.ivashkin@phystech.edu',
        'session_key': 'illusionww.play@gmail.com',
        'session_password': 'La12m10p7',
        'isJsEnabled': 'false',
        'submit': 'Войти'
    }

    def __init__(self):
        self.statistics = {
            'new': 0,
            'noname': 0,
            'noavatar': 0
        }
        self.people = {}

        self.session = FuturesSession(max_workers=10)
        future_one = self.session.get(self.root_url, headers=self.headers)
        response_one = future_one.result()
        soup = BeautifulSoup(response_one.text, "html.parser")
        login_data = LinkedinSearchParser.login_static_data.copy()
        login_data['loginCsrfParam'] = soup.find(id="loginCsrfParam-login")['value']
        login_data['sourceAlias'] = soup.find(id="sourceAlias-login")['value']
        self.session.post(self.login_submit_url, headers=self.headers, data=login_data)

    def get_100search_pages(self, static_params):
        print("get_100search_pages", static_params)
        futures = []
        for i in range(1, 101):
            params = static_params.copy()
            params['page_num'] = str(i)
            future = self.session.get(self.search_url,
                                      headers=self.headers,
                                      params=params,
                                      background_callback=self.process_search_page)
            futures.append(future)
        for i in range(100):
            response = futures[i].result()
            self.people.update(response.parsed_people)

    def process_search_page(self, sess, resp):
        resp.parsed_people = {}
        try:
            info = resp.json()
        except Exception:
            print('beda')
            return

        page_statistics = {
            'new': 0,
            'noname': 0,
            'noavatar': 0
        }

        for item in info['content']['page']['voltron_unified_search_json']['search']['results']:
            item = item['person']
            person_id = item['id']
            if person_id not in self.people:
                page_statistics['new'] += 1
                if 'firstName' not in item or 'lastName' not in item:
                    page_statistics['noname'] += 1
                    person = {
                        "id": person_id,
                        "condition": "noname"
                    }
                elif 'media_picture_link_100' not in item['logo_result_base']:
                    page_statistics['noavatar'] += 1
                    person = {
                        "id": person_id,
                        "first_name": item['firstName'],
                        "last_name": item['lastName'],
                        "condition": "noavatar"
                    }
                else:
                    person = {
                        "id": person_id,
                        "first_name": item['firstName'],
                        "last_name": item['lastName'],
                        "img_url": item['logo_result_base']['media_picture_link_100'],
                        "condition": "OK"
                    }
                resp.parsed_people[person_id] = person
                self.statistics["new"] += page_statistics["new"]
                self.statistics["noname"] += page_statistics["noname"]
                self.statistics["noavatar"] += page_statistics["noavatar"]


def main():
    print(datetime.now(), "STEP 1: Get data from search...")
    search_parser = LinkedinSearchParser()
    with open('step1.json') as data_file:
        search_parser.people = json.load(data_file)

    search_parser.get_100search_pages({'type': 'people', 'f_I': '12'})
    for usa_num in range(100):
        search_parser.get_100search_pages({'type': 'people', 'f_I': '12', 'f_G': 'us:' + str(usa_num)})
        search_parser.statistics["count"] = len(search_parser.people)
        print(search_parser.statistics)
        with open('step1.json', 'w') as outfile:
            json.dump(search_parser.people, outfile)
    print(datetime.now(), "DONE: Get data from search")


if __name__ == "__main__":
    main()
