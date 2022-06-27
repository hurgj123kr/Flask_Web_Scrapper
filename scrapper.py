import requests
from bs4 import BeautifulSoup

Page_count = 50

def public_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return soup


def get_last_page(url):
    url = public_page(url)
    pages = url.find("div", {"class": "pagination"}).find_all("a")
    last_page = pages[-1].string
    if last_page == '다음':
        last_page = pages[-2].string
    else:
        int(last_page)
    return int(last_page)


def extract_job(html):
    title = html.find("h2", {"class": "job_tit"}).find("a")["title"]
    company = html.find("div", {
        "class": "area_corp"
    }).find("a", {
        "class": "track_event data_layer"
    }).get_text(strip=True)
    location = html.find("div", {
        "class": "job_condition"
    }).find("span").get_text(strip=True).strip()
    job_id = html.get("value")
    return {
        "title":
        title,
        "company":
        company,
        "location":
        location,
        "link":
        f"https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx={job_id}#seq=0"
    }



def page_list(last_page,word):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Saramin Page: {page}")
        result = requests.get(
            f"https://www.saramin.co.kr/zf_user/search/recruit?searchword={word}&searchType=connect&search_done=y&recruitPage={page +1}&recruitSort=relation&recruitPageCount={Page_count}"
        )
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class": "item_recruit"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&keydownAccess=&searchword={word}&panel_type=&search_optional_item=y&search_done=y&panel_count=y&recruitPage=1&recruitSort=relation&recruitPageCount={Page_count}"
    last_page = get_last_page(url)
    jobs = page_list(last_page,word)
    return jobs
