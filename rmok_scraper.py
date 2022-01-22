import requests
from bs4 import BeautifulSoup


def extract_job(html):
    try:
      company = html.attrs['data-company']
      title = html.find("h2", itemprop="title").get_text(strip=True)
      tooltips = html.find_all("div", class_="location")
      region, pay = ['No information','No information']
      if len(tooltips) == 2:
        region = tooltips[0].get_text(strip=True)
        pay = tooltips[1].get_text(strip=True)
      else:
        for tooltip in tooltips:
          if '💰' in tooltip.string:
            pay = tooltip.get_text(strip=True)
          else:
            region = tooltip.get_text(strip=True)
      tag_str = ""
      tags = html.find_all("div", class_="tag")
      for tag in tags:
        tag_str = tag_str + " #" + tag.find("h3").get_text(strip=True)
      url = html.find("td", class_="source").find("a")['href']
    except:
      pass
    return {
        'site': 'RemoteOK',
        'title': title,
        'company': company,
        'location': region,
        'apply_link': f"https://remoteok.com{url}",
        'worktime': 'No Information',
        'pay': pay,
        'tag': tag_str
    }

def get_jobs(word):
  jobs = []
  try: 
    url = f"https://remoteok.io/remote-{word}-jobs"
    print(f"Scrapping RemoteOK")
    headers = { 'Accept-Language' : "en-US,en;q=0.9,ko;q=0.8",
                'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
    result = requests.get(url, headers = headers)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find("table", id="jobsboard").find_all("tr", class_="job")
    for result in results:
        job = extract_job(result)
        jobs.append(job)
  except:
    pass
  return jobs
