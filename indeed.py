import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=machine+learning&limit={LIMIT}"

def extract_indeed_pages():
    result = requests.get(URL)

    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div",{"class":"pagination"})

    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = max(pages)

    return max_page

def extract_jobs(html):
    title = html.find('h2').find('a')["title"]
    company = html.find("span", {"class": "company"})
    company_ancor = company.find("a")
    if company_ancor is not None:
        company = str(company.find("a").string)
    else:
        company = str(company.string)
    company = company.strip()
    location = html.find("div", {"class": "recJobLoc"})['data-rc-loc']
    job_id = html['data-jk']
    return {'title':title, 'company':company, 'location':location,'link':f"https://www.indeed.com/viewjob?jk={job_id}"}

def extract_indeed_jobs(last_pages):
    jobs = []
    for page in range(last_pages):
        print(f"Scrapping page {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        job_results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for job_result in job_results:
            job = extract_jobs(job_result)
            jobs.append(job)
    return jobs