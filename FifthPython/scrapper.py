import requests
from bs4 import BeautifulSoup



def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find("a", {"class": "s-link"})
    if title is None:
        return -1
    else:
        title = title.get_text(strip=True)
    location = html.find("div",{"class": "flex--item fc-black-500 fs-body1"})
    if location is None:
        return -1
    else:
        location = location.get_text(strip=True)
        # company = .get_text(strip=True)
    company = html.find("svg",{"class": "ps-relative tn2 svg-icon iconIndustry"}).find_parent('div')
    print(company)
    if company is None:
        return -1
    else:
        company = company.get_text(strip=True)
    job_id = html.find("a", {"class": "s-link"})["href"]
    if job_id is None:
        return -1
    else:
        job_id = job_id
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://stackoverflow.com{job_id}"
    }


def extract_jobs(last_page,url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.select("div", {"class": "d-flex"})
        for result in results:
            job = extract_job(result)
            if job == -1:
                continue
            jobs.append(job)
    return jobs


def get_jobs(word):
  url = f"https://stackoverflow.com/jobs/companies?q={word}"
  last_page = get_last_page(url)
  jobs=[]  
  jobs.append(extract_jobs(last_page,url))
  return jobs
