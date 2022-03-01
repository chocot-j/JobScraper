import requests
from bs4 import BeautifulSoup

def get_rok_job(search_word, user_agent):
  headers = {"User-Agent": user_agent}
  rok_url = f"https://remoteok.com/remote-{search_word}-jobs"
  rok_jobs = []
  
  try:
    res = requests.get(rok_url, headers=headers)
    if res.status_code != 200:
      print(f"rok response: {res.status_code}")
      if res.status_code != 301:
        raise requests.exceptions.RequestException
  except:
    print("Request Error: rok_job")
    return rok_jobs
  soup = BeautifulSoup(res.text, "html.parser")

  job_rows = soup.select("tr.job")
  for job_row in job_rows:
    company = job_row.select_one("td.company > span > h3")
    if company:
      company = company.get_text(strip=True)
    title = job_row.select_one("td.company > a > h2")
    if title:
      title = title.get_text(strip=True)
    place_list = job_row.select("td.company > div.location")
    if place_list:
      if len(place_list) == 2:
        place = place_list[0].get_text(strip=True)
      else:
        place = "None"
    else:
      place = "None"
    date = job_row.select_one("td.time > time")
    if date:
      date = date.get_text(strip=True)
    link_part = job_row["data-url"]
    link = f"https://remoteok.com{link_part}"
    company_img = job_row.select_one("td.has-logo> a > img.logo")
    if company_img:
      company_img = company_img["data-src"]

    job = {
      "company": company,
      "title": title,
      "place": place,
      "date": date,
      "link": link,
      "company_img": company_img,
    }
    rok_jobs.append(job)

  return rok_jobs