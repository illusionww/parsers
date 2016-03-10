import requests
from bs4 import BeautifulSoup


class LinkedinNoAuthProfileParser(object):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}

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
                  'location': demographics.find("span", "locality").text,
                  'industry': demographics.find_all("dd", "descriptor")[1].text
                  if len(demographics.find_all("dd", "descriptor")) > 1 else None}

        if "no-picture" not in profile_card["class"]:
            person['picture_url'] = profile_card.find("div", "profile-picture").a.img['data-delayed-url']

        # SECTION: summary
        summary_section = soup.find(id="summary")
        if summary_section:
            person['summary'] = summary_section.find("div", "description").p.text

        # SECTION: experience
        experience_section = soup.find(id="experience")
        if experience_section:
            person['positions'] = self.parse_section(experience_section, "position", "organization", "currentPositions")

        # SECTION: education
        education_section = soup.find(id="education")
        if education_section:
            person['educations'] = self.parse_section(education_section, "university", "degree", None)
        return person

    @staticmethod
    def parse_section(section, title_name, subtitle_name, is_current_condition):
        return [{title_name: item.find("h4", "item-title").text,
                 subtitle_name: item.find("h5", "item-subtitle").text,
                 "date_range": item.find("span", "date-range").text
                 if item.find("span", "date-range") else None,
                 "description": item.find("div", "description").p.text
                 if item.find("div", "description") else None,
                 "is_current": item["data-section"] == is_current_condition
                 if is_current_condition else None
                 } for item in section.find_all("li")]


def main():
    parser = LinkedinNoAuthProfileParser()
    person = parser.get_person_info_by_link("https://www.linkedin.com/in/ivashkin")
    print(person)


if __name__ == "__main__":
    main()
