import requests
from bs4 import BeautifulSoup


class LinkedinSearch(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }

    def get_persons_by_name(self, first_name, last_name):
        url = 'http://www.linkedin.com/pub/dir/' + first_name + '/' + last_name + '/'
        page = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(page, "html.parser")
        return [self.get_person_info_by_link(profile.find("div", "content").h3.a['href'])
                for profile in soup.find_all('div', 'profile-card')]

    def get_person_info_by_link(self, url):
        print("processing", url)  # for debugging purposes

        page = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(page, "html.parser")

        # SECTION: topcard
        section_topcard = soup.find(id="topcard")
        profile_card = section_topcard.find("div", "profile-card")
        profile_overview_content = profile_card.find("div", "profile-overview-content")
        demographics = profile_overview_content.find(id="demographics")
        person = {'link': url,
                  'name': profile_overview_content.find(id="name").text,
                  'headline': profile_overview_content.find("p", "headline").text
                  if profile_overview_content.find("p", "headline") else None,
                  'locality': demographics.find("span", "locality").text,
                  'industry': demographics.find_all("dd", "descriptor")[1].text
                  if len(demographics.find_all("dd", "descriptor")) > 1 else None,
                  'member_connections': profile_overview_content.find("div", "member-connections").strong.text}

        if "no-picture" not in profile_card["class"]:
            person['picture_url'] = profile_card.find("div", "profile-picture").a.img['data-delayed-url']

        # SECTION: summary
        summary_section = soup.find(id="summary")
        if summary_section:
            person['summary'] = summary_section.find("div", "description").p.text

        # SECTION: experience
        experience_section = soup.find(id="experience")
        if experience_section:
            person['positions'] = [{'position': position.find("h4", "item-title").a.text,
                                    'organization': position.find("h5", "item-subtitle").a.text
                                    if position.find("h5", "item-subtitle").a else None,
                                    'data-range': position.find("span", "date-range").text
                                    if position.find("span", "date-range") else None,
                                    "description": position.find("p", "description").text
                                    if position.find("p", "description") else None
                                    } for position in experience_section.find_all("li", "position")]

        # SECTION: certifications
        # skip

        # SECTION: volunteering
        # skip

        # SECTION: recommendations
        # skip

        # SECTION: languages
        languages_section = soup.find(id="languages")
        if languages_section:
            person['languages'] = [{'name': language.find("h4", "name").text,
                                    'proficiency': language.find("p", "proficiency").text
                                    } for language in languages_section.find_all("li", "language")]
        # SECTION: projects
        # skip

        # SECTION: skills
        skills_section = soup.find(id="skills")
        if skills_section:
            person['skills'] = [skill.a["title"] for skill in skills_section.ul.find_all("li", "skill")
                                if not any(x in skill["class"] for x in ["see-less", "see-more"])]

        # SECTION: education
        education_section = soup.find(id="education")
        if education_section:
            person['educations'] = [{"university": education.find("h4", "item-title").text,
                                     "degree": education.find("h5", "item-subtitle").text,
                                     "data-range": education.find("span", "date-range").text
                                     if education.find("span", "date-range") else None,
                                     "description": education.find("div", "description").p.text
                                     if education.find("div", "description") else None
                                     } for education in education_section.find_all("li", "school")]
        return person


def main():
    first_name, last_name = "Sergey Petrov".split()

    linkedin_search = LinkedinSearch()
    persons = linkedin_search.get_persons_by_name(first_name, last_name)
    for person in persons:
        print(person)


if __name__ == '__main__':
    main()
