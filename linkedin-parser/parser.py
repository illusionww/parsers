import requests
from bs4 import BeautifulSoup


class LinkedinSearch(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }

    def find_list_by_name(self, first_name, last_name):
        url = 'http://www.linkedin.com/pub/dir/' + first_name + '/' + last_name + '/'
        page = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(page, "html.parser")
        for profile in soup.find_all('div', 'profile-card'):
            link = profile.find("div", "content").h3.a['href']
            self.get_all_info_by_link(link)

    def get_all_info_by_link(self, url):
        page = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(page, "html.parser")

        # SECTION: topcard
        demographics = soup.find(id="demographics")
        person = {'name': soup.find(id="name").text,
                  'picture_url': soup.find("div", "profile-picture").a.img['data-delayed-url'],
                  'locality': demographics.find("span", "locality").text,
                  'industry': demographics.find_all("dd", "descriptor")[1].text,
                  'member_connections': soup.find("div", "member-connections").strong.text}

        # SECTION: experience
        experience_section = soup.find(id="experience")
        person['positions'] = [{'position': position.find("h4", "item-title").a.text,
                                       'organization': position.find("h5", "item-subtitle").a.text,
                                        'data-range': position.find("span", "date-range").text
                                        } for position in experience_section.find_all("li", "position")]

        # SECTION: volunteering
        # skip

        # SECTION: languages
        languages_section = soup.find(id="languages")
        person['languages'] = [{'name': language.find("h4", "name").text,
                                'proficiency': language.find("p", "proficiency").text
                                } for language in languages_section.find_all("li", "language")]
        # SECTION: projects
        # skip

        # SECTION: skills
        skills_section = soup.find(id="skills")
        person['skills'] = [skill.a["title"] for skill in skills_section.ul.findChildren("li", "skill") if not any(x in skill["class"] for x in ["see-less", "see-more"])]

        # SECTION: education
        education_section = soup.find(id="education")
        person['educations'] = [{"university": education.find("h4", "item-title").text,
                                 "degree": education.find("h5", "item-subtitle").text,
                                 "data-range": education.find("span", "date-range").text
                                 } for education in education_section.findChildren("li", "school")]

        print(person)


def main():
    first_name, last_name = "Vladimir Ivashkin".split()

    linkedin_search = LinkedinSearch()
    linkedin_search.find_list_by_name(first_name, last_name)


if __name__ == '__main__':
    main()
