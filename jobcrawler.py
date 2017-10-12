import json
from sys import exit, maxsize

import requests
from lxml import html


class ResultItem():
    """
        Represent a result from search query
    """

    def __init__(self, _title=None, _company=None, _location=None, _date=None, _link=None, _description=None, _desired_experience=None):
        self._title = _title
        self._company = _company
        self._location = _location
        self._date = _date
        self._link = _link
        self._description = _description
        self._desired_experience = _desired_experience

    @property
    def title(self):
        return self._title

    @property
    def company(self):
        return self._company

    @property
    def location(self):
        return self._location

    @property
    def link(self):
        return self._link

    @property
    def description(self):
        return self._description

    @property
    def desired_experience(self):
        return self._desired_experience

HOST = 'https://www.indeed.com'


def search_job_indeed(keyword, location=None, zipcode=None, distance=None, max_no_result=maxsize, output_filename='data.json'):

    visited_url = set({})

    start_url = f'https://www.indeed.com/jobs?q={keyword}&l={location}&radius={distance}'
    visited_url.add(start_url)
    jobs = []
    next_url = start_url
    result_count = 0
    while next_url and result_count < max_no_result:
        try:
            page = requests.get(next_url)
        # At the moment, we just capture all exception, may be handle later
        except Exception as ex:
            break

        tree = html.fromstring(page.content)
        rows = tree.xpath(
            '//div[contains(@class, "row") and contains(@class, "result")]')

        for row in rows:
            item = extract_data(row)
            result_count += 1
            if result_count > max_no_result:
                break

            # If have job post
            if item.title:
                # Do with scraped item
                json_obj = {
                    "title": item.title,
                    "company": item.company,
                    "job_location": item.location,
                    "description": item.description,
                    "desired_experience": item.desired_experience,
                    "link": item.link
                }
                jobs.append(json_obj)

        next_url = tree.xpath(
            '//a[span[span[@class="np" and contains(text(),"Next")]]]/@href')

        # If next url is visited before then quit
        if next_url and next_url[0] not in visited_url:
            next_url = HOST + next_url[0]
            visited_url.add(next_url)
        else:
            next_url = None

    # Save jobs to json file
    with open(output_filename, 'a+') as f:
        json.dump(jobs, f)


def extract_data(row):
    title = row.xpath('.//h2[@class="jobtitle"]/a/text()')
    # result from xpath function is a list, we take first element
    title = title[0] if title else ''

    link = row.xpath('.//h2[@class="jobtitle"]/a/@href')
    link = HOST + link[0] if link else ''

    company = row.xpath(
        './/span[@class="company"]/span[@itemprop="name"]/a/text()')
    if not company:
        company = row.xpath(
            './/span[@class="company"]/span[@itemprop="name"]/text()')
    company = company[0] if company else ''
    # print(company)
    job_location = row.xpath(
        './/span[@itemprop="jobLocation"]/span/span/text()')
    job_location = job_location[0] if job_location else ''

    description = row.xpath(
        './/div/span[@class="summary" and @itemprop="description"]/text()')
    description = description[0] if description else ''

    desired_experience = row.xpath(
        './/div[@class="experience"]/span[@class="experienceList"]/text()')
    desired_experience = desired_experience[0] if desired_experience else ''

    return ResultItem(_title=title, _company=company, _location=job_location, _date=None, _link=link, _description=description, _desired_experience=desired_experience)


if __name__ == '__main__':
    print("""
        You CAN leave empty in any field below
        Ctrl + Z -> Enter to quit
    """)

    try:
        keyword = input("Please enter the keyword (default is Python)  ") or 'Python'
        location = input("Please enter the location (empty means any where)  ")
        max_result = input("Max result (empty means as much as posible)  ")
        max_result = int(max_result) if max_result else maxsize
        output = input("Output file (default: data.json)  ") or 'data.json'
        search_job_indeed(keyword, location, max_no_result=max_result)
    # Ctrl+Z causes EOFError
    except EOFError as identifier:
        exit(1)
