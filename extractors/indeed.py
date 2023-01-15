from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_page_count(keyword):
  options = Options()
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  browser = webdriver.Chrome(options=options)

  base_url = "https://kr.indeed.com/jobs?q="
  end_url = "&limit=50"
  browser.get(f"{base_url}{keyword}{end_url}")
  soup = BeautifulSoup(browser.page_source,"html.parser")
  pagination = soup.find("nav", class_="ecydgvn0")
  if pagination == None: #정보 없을때
    return 1
  pages = pagination.find_all("div", recursive=False)
  count = len(pages)
  if count == 0:
    return 1
  elif count >= 5:
    return count - 1
  else:
    return count + 1
    
def extract_indeed_jobs(keyword):
  options = Options()
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  browser = webdriver.Chrome(options=options)

  pages= get_page_count(keyword)
  print("Found",pages, "pages")
  results = []
  
  for page in range(pages):
    base_url = "https://kr.indeed.com/jobs"
    end_url = "&limit=50"
    final_url = f"{base_url}?q={keyword}&start={page*10}{end_url}"
    print(final_url)
    browser.get(final_url)
  
    soup = BeautifulSoup(browser.page_source, "html.parser")
    job_list = soup.find("ul", class_="jobsearch-ResultsList")
  
    jobs = job_list.find_all('li', recursive=False)
  
    for job in jobs:
      zone = job.find("div", class_="mosaic-zone")
      if zone == None:
        anchor = job.select_one("h2 a")
        title = anchor['aria-label']
        link = anchor['href']
        company = job.find("span", class_="companyName")
        location = job.find("div", class_="companyLocation")
        job_data = {
          'link': f"https://kr.indeed.com{link}",
          'company': company.string,
          'location': location.string,
          'position': title
        }
        results.append(job_data)
  return results