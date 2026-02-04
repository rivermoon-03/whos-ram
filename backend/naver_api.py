import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

# #region agent log
print(f"🔍 DEBUG: NAVER_CLIENT_ID exists: {NAVER_CLIENT_ID is not None}")
print(f"🔍 DEBUG: NAVER_CLIENT_ID length: {len(NAVER_CLIENT_ID) if NAVER_CLIENT_ID else 0}")
print(f"🔍 DEBUG: NAVER_CLIENT_SECRET exists: {NAVER_CLIENT_SECRET is not None}")
print(f"🔍 DEBUG: NAVER_CLIENT_SECRET length: {len(NAVER_CLIENT_SECRET) if NAVER_CLIENT_SECRET else 0}")
if NAVER_CLIENT_ID:
    print(f"🔍 DEBUG: NAVER_CLIENT_ID first 5 chars: {NAVER_CLIENT_ID[:5]}...")
if NAVER_CLIENT_SECRET:
    print(f"🔍 DEBUG: NAVER_CLIENT_SECRET first 5 chars: {NAVER_CLIENT_SECRET[:5]}...")
# #endregion


def search_shop(query: str, display: int = 10, start: int = 1, sort: str = "sim"):
    # #region agent log
    print(f"🔍 DEBUG: search_shop called with query: {query}")
    # #endregion
    
    # 환경 변수 확인
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        error_msg = f"❌ 네이버 API 인증 정보가 설정되지 않았습니다. NAVER_CLIENT_ID: {'설정됨' if NAVER_CLIENT_ID else 'None'}, NAVER_CLIENT_SECRET: {'설정됨' if NAVER_CLIENT_SECRET else 'None'}"
        print(error_msg)
        raise ValueError(error_msg)
    
    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    
    # #region agent log
    print(f"🔍 DEBUG: API request headers - Client-ID is None: {NAVER_CLIENT_ID is None}, Client-Secret is None: {NAVER_CLIENT_SECRET is None}")
    print(f"🔍 DEBUG: API request headers - Client-ID empty: {NAVER_CLIENT_ID == '' if NAVER_CLIENT_ID else 'N/A'}, Client-Secret empty: {NAVER_CLIENT_SECRET == '' if NAVER_CLIENT_SECRET else 'N/A'}")
    # #endregion
    
    params = {"query": query, "display": display, "start": start, "sort": sort}

    response = requests.get(url, headers=headers, params=params)
    
    # #region agent log
    print(f"🔍 DEBUG: API response status_code: {response.status_code}")
    if response.status_code != 200:
        print(f"🔍 DEBUG: API response text: {response.text[:200]}")
    # #endregion
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
