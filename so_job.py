import requests
from bs4 import BeautifulSoup

def get_last_page(so_url):
  # request site first page
  try:
    so_res = requests.get(so_url)
    if so_res.status_code != 200:
      raise requests.exceptions.RequestException
  except:
    print("Request Error: so_job")
    return 0
  so_soup = BeautifulSoup(so_res.text, "html.parser")

  # find last page number
  last_page = so_soup.select("div.s-pagination > a")[-2].get_text(strip=True)

  return int(last_page)


def get_so_job(search_word):
  so_url = f"https://stackoverflow.com/jobs/?q={search_word}"
  last_page = get_last_page(so_url)
  so_jobs = []
  
  # get jobs from each page
  for page in range(last_page):
    try:
      res = requests.get(f"{so_url}&pg={page + 1}")
    except:
      print(f"Request Error: so_job: page {page + 1}")
      continue
    soup = BeautifulSoup(res.text, "html.parser")

    job_rows = soup.select("div.listResults > div.-job")
    for job_row in job_rows:
      company = job_row.select_one("h3.fs-body1 > span")
      if company:
        company = company.get_text(strip=True)
      title = job_row.select_one("h2 > a")
      if title:
        title = title["title"]
      place = job_row.select_one("h3.fs-body1 > span.fc-black-500")
      if place:
        place = place.get_text(strip=True)
      else:
        place = "None"
      date = job_row.select_one("ul > li:first-child > span")
      if date:
        date = date.get_text(strip=True)
      job_code = job_row["data-jobid"]
      link = f"https://stackoverflow.com/jobs/{job_code}/?q={search_word}"
      company_img = job_row.select_one("div.d-flex > div.s-avatar > img")
      if company_img:
        company_img = company_img["src"]
      
      job = {
        "company": company,
        "title": title,
        "place": place,
        "date": date,
        "link": link,
        "company_img": company_img,
      }
      so_jobs.append(job)
  
  return so_jobs
