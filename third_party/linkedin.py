import os #환경 번수 접근
import requests #api에 http 요청 보냄
from dotenv import load_dotenv

load_dotenv()

'''
linkedin을 Scraping 하는 형식
함수는 링크드인의 정보를 가져와 HTTP 요청으로
Linkedin 정보를 스크래핑해주는 Proxy Curl이라는 외부 API를 사용
'''
def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/wjdengus98/a89ee9b012552221e7099ca6810525f7/raw/3c0a5be5894ae0e5e9b31334a208cb081e07f6c0/hyun-doo.json"
        response = requests.get(linkedin_profile_url,timeout=10)
    else:
        api_endpoint = "https://api.scrapin.io/v1/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl" : linkedin_profile_url
        }

        response = requests.get(
            api_endpoint,
            params = params,
            timeout = 20
        )

    data = response.json().get("person")
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None) and k not in ["certifications"]
    }

    return data

if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/hyundoo-jeong-9b58b4284/"
        ),
    )