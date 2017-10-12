## Job crawler
Job crawler with keyword, location

### Fields to be crawled
* job title
* company
* job location
* job description
* job desired experience
* link to job detail 

Output data is json

```json
[
  {
    "title": "Bioinformaticist - Genomics, Amazon Web Services",
    "company": "\nAmazon Web Services, Inc.",
    "job_location": "Seattle, WA",
    "description": "\nRelevant technical knowledge such as R, RStudio, algorithmic development with ",
    "desired_experience": "R, Perl, Python, AWS",
    "link": "https://www.jobwebpage.com/rc/clk?jk=15598753da8626ba&fccid=fe2d21eef233e94a"
  },
  {
    "title": "Data Scientist | San Francisco | Model Development Group",
    "company": "\nCarbon Lighthouse",
    "job_location": "San Francisco, CA",
    "description": "\nConversant with data science libraries within ",
    "desired_experience": "Machine Learning, R, Data Science, Python",
    "link": "https://www.jobwebpage.com/rc/clk?jk=11dd6466668b877c&fccid=a8605dd2196da447"
  }
]
```
### Install

```bash
    virtualenv --python=python3.5 venv
    source venv/bin/activate
    pip install request
    pip install lxml

    # Run it
    python jobcrawler.py
```