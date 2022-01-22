import requests
from bs4 import BeautifulSoup


def get_section(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    sections = soup.find("div", id="job_list").find_all("section", class_="jobs")
    return sections


def extract_job(html, category):
    try:
      company, worktime, region = html.find_all("span", class_="company")
      company = company.get_text(strip=True)
      worktime = worktime.get_text(strip=True)
      region = region.get_text(strip=True)
      title = html.find("span", class_="title").get_text(strip=True)
      job = html.find_all('a')[1]
      url = job.attrs['href']
    except:
      pass
    return {
        'site': 'WeWorkRemotely',
        'title': title,
        'company': company,
        'location' : region,
        'apply_link': f"https://weworkremotely.com{url}",
        'worktime': worktime,
        'pay': 'No Information',
        'tag': 'No Information'
        
    }


def extract_jobs(sections, url):
    jobs = []
    for section in sections:

      category = section.find("h2").find("a").string
      if category == "Full-Stack Programming Jobs":
        category = "Full-Stack"
      elif category == "Front-End Programming Jobs":
        category = "Front-End"
      elif category == "Back-End Programming Jobs":
        category = "Back-End"
      else:
        category = "All other jobs"

      print(f"Scrapping WWR : {category} category")
      result = requests.get(url)
      soup = BeautifulSoup(result.text, "html.parser")
      results = soup.find_all("li", class_="feature")
      for result in results:
          job = extract_job(result, category)
          jobs.append(job)
    return jobs


def get_jobs(word):
  jobs = []
  try:
    url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
    sections = get_section(url)
    jobs = extract_jobs(sections, url)
  except:
    pass
  return jobs
