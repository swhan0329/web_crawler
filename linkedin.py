import requests
from bs4 import BeautifulSoup

LIMIT = 20
URL = f"http://search.incruit.com/list/search.asp?col=job&il=y&kw=machine+learning"

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("p",{"class":"sqr_paging sqr_pg_mid"})
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = max(pages)

    return max_page

def extract_jobs(html):
    title = html.find("span", {"class": "rcrtTitle"}).text
    company = html.find("h3")
    if company:
        company_ancor = company.find("a")
        if company_ancor is not None:
            company = str(company.find("a").string)
        else:
            company = str(company.string)
        company = company.strip()
    else:
        company = None
    location = html.find("p", {"class": "etc"}).find('span').string.split('|')[1]
    job_id_html = html.find("p", {"class": "detail"}).find('button')
    job_id = job_id_html['f_job']
    return {'title':title, 'company':company, 'location':location,'link':f"http://job.incruit.com/jobdb_info/jobpost.asp?job={job_id}"}

def get_jobs(last_pages):
    jobs = []
    for page in range(last_pages):
        print(f"Scrapping page {page}")
        result = requests.get(f"{URL}&startno={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        job_results = soup.find("ul", {"class": "litype01"}).find_all("li")
        for job_result in job_results:
            job = extract_jobs(job_result)
            jobs.append(job)
    return jobs

def get_whole_jobs():
    last_page = get_last_page()
    jobs = get_jobs(last_page)

    return jobs

