import requests
from bs4 import BeautifulSoup

START_PAGE = "https://www.linkedin.com/directory/people-{}"


def step_into(url, name):
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    page_links = [(item.string, item['href']) for item in soup.findAll('a', href=True)]
    for link in page_links:
        if link[1].startswith(url):
            pos = link[0].find(" - ")
            if pos != -1:
                left_border, right_border = link[0][:pos], link[0][pos + 3:]
                left_border, right_border = left_border.strip(), right_border.strip()
                if left_border <= name <= right_border:
                    print link[0], link[1]
                    step_into(link[1][:-1], name)
                    return
    print url


def main():
    name = raw_input()
    step_into(START_PAGE.format(name[0]).lower(), name)


if __name__ == '__main__':
    main()
