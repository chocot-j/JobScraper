import requests
from bs4 import BeautifulSoup

def get_wwr_job(search_word):
  wwr_url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={search_word}"
  wwr_jobs = []

  try:
    res = requests.get(wwr_url)
    if res.status_code != 200:
      raise requests.exceptions.RequestException
  except:
    print("Request Error: wwr_job")
    return wwr_jobs
  soup = BeautifulSoup(res.text, "html.parser")

  # get jobs from each section
  job_boxes = soup.select("div#job_list > section")
  for job_box in job_boxes:
    job_rows = job_box.select("ul > li")
    job_rows = job_rows[:-2]    
    for job_row in job_rows:
      company = job_row.select_one("a > span.company")
      if company:
        company = company.get_text(strip=True)
      title = job_row.select_one("a> span.title")
      if title:
        title = title.get_text(strip=True)
      place = job_row.select_one("a > span.region company")
      if place:
        place = place.get_text(strip=True)
      else:
        place = "None"
      date = job_row.select_one("a > span.date > time")
      if date:
        date = date.get_text(strip=True)
      link_part = job_row.select_one("li > a")["href"]
      link = f"https://weworkremotely.com{link_part}"
      company_img = job_row.select_one("div.tooltip > a > div.flag-logo")
      if company_img:
        company_img = company_img["style"].lstrip("background-image:url").strip("()")
      
      job = {
        "company": company,
        "title": title,
        "place": place,
        "date": date,
        "link": link,
        "company_img": company_img,
      }
      wwr_jobs.append(job)
      
  return wwr_jobs
  