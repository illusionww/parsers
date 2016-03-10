import requests
from bs4 import BeautifulSoup
from requests.exceptions import ChunkedEncodingError


class LinkedinNoAuthTop25ByNameParser:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
    top25_url = 'https://www.linkedin.com/pub/dir/{}/{}/'

    def get_people_by_name(self, first_name, last_name):
        url = self.top25_url.format(first_name, last_name)
        try:
            response = requests.get(url, headers=self.headers)
        except ChunkedEncodingError:
            print("Incomplete read(")
            return []
        if response.history:  # if there are only one person with this name linkedin redirects you to his page
            person = {
                'name': first_name + " " + last_name,
                'url': response.url,
            }
            return [person]
        else:
            page = response.text
            soup = BeautifulSoup(page, "html.parser")

            people = []
            for profile in soup.find_all('div', 'profile-card'):
                content = profile.find("div", "content")
                img_url = profile.find("a", "profile-img").img['src']
                person = {
                    'name': content.h3.a.text,
                    'url': content.h3.a['href'],
                    # 'headline': content.find('p', "headline").text,
                    # "location": content.find("dl", "basic").findAll("dd")[0].text,
                    # 'industry': content.find("dl", "basic").findAll("dd")[1].text,
                    'img_url': img_url if "ghost" not in img_url else "ghost"
                }
                people.append(person)
            return people


def main():
    parser = LinkedinNoAuthTop25ByNameParser()
    people = parser.get_people_by_name("Vladimir", "Ivashkin")
    # people = parser.get_people_by_name("Taras", "Pustovoy")
    for person in people:
        print(person)


if __name__ == "__main__":
    main()
