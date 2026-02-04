import os
import requests
from dotenv import load_dotenv

load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")


def search_shop(query: str, display: int = 10, start: int = 1, sort: str = "sim"):
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        error_msg = f"네이버 API 인증 정보가 설정되지 않았습니다. NAVER_CLIENT_ID: {'설정됨' if NAVER_CLIENT_ID else 'None'}, NAVER_CLIENT_SECRET: {'설정됨' if NAVER_CLIENT_SECRET else 'None'}"
        raise ValueError(error_msg)
    
    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    params = {"query": query, "display": display, "start": start, "sort": sort}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
