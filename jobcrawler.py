import json
from sys import maxsize

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
        page = requests.get(next_url)
        tree = html.fromstring(page.content)
        rows = tree.xpath('//div[contains(@class, "row") and contains(@class, "result")]')

        for row in rows:
            item = extract_data(row)
            result_count += 1
            if result_count > max_no_result:
                break

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
        
        next_url = tree.xpath('//a[span[span[@class="np" and contains(text(),"Next")]]]/@href')
        if next_url and next_url[0] not in visited_url:
            next_url = next_url[0]
            visited_url.add(next_url)
        else:
            next_url = None

    with open(output_filename, 'a+') as f:
        json.dump(jobs, f)


def extract_data(row):
    title = row.xpath('.//h2[@class="jobtitle"]/a/text()')
    title = title[0] if title else ''

    link = row.xpath('.//h2[@class="jobtitle"]/a/@href')
    link = HOST + link[0] if link else ''

    company = row.xpath(
        './/span[@class="company"]/span[@itemprop="name"]/a/text()')
    if not company:
        company = row.xpath(
                './/span[@class="company"]/span[@itemprop="name"]/text()')
    company = company[0] if company else ''

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
    # keyword = input("Please enter the keyword, example: python ") or 'python'
    # location = input("Please enter the location, example 'San Diego' ")
    # max_result = input("Leave empty if you want to scrap as much as posible: ")
    # max_result = int(max_result) if max_result else maxsize
    # search_job_indeed(keyword, location)
    search_job_indeed('python', 'San Diego', max_no_result=1)
