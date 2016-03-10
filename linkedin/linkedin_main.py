import json
from datetime import datetime

from linkedin_profile_parser import LinkedinNoAuthProfileParser
from linkedin_top25byname_parser import LinkedinNoAuthTop25ByNameParser


def main():


    print(datetime.now(), "STAGE 2: Get top25 for each person...")
    statistics = {
        'found_profiles': 0,
        'not_in_top25': 0,
        'unique': 0
    }
    top25_parser = LinkedinNoAuthTop25ByNameParser()
    people_st2 = []
    for person in people_st1.values():
        top25_people = top25_parser.get_people_by_name(person['first_name'], person['last_name'])
        if len(top25_people) > 1:
            found = False
            for top25_person in top25_people:
                if top25_person["img_url"] == person["img_url"]:
                    statistics["found_profiles"] += 1
                    people_st2.append(top25_person)
                    found = True
                    break
            if not found:
                statistics['not_in_top25'] += 1
        elif len(top25_people) == 1:
            statistics["unique"] += 1
            people_st2.append(top25_people[0])
    print(datetime.now(), "DONE: Get top25 for each person")
    print(statistics)

    print(datetime.now(), "STAGE 3: Get profiles...")
    people_st3 = []
    profile_parser = LinkedinNoAuthProfileParser()
    for people_for_url in people_st2:
        url = people_for_url["url"]
        try:
            profile = profile_parser.get_person_info_by_link(url)
            people_st3.append(profile)
        except AttributeError:
            print("Attribute Error in", url)
    print("DONE: Get profiles...")

    with open('data.txt', 'w') as outfile:
        json.dump(people_st3, outfile)

if __name__ == "__main__":
    main()