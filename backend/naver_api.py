import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

# #region agent log
log_path = "/home/rivermoon/Documents/Github/.cursor/debug.log"
try:
    with open(log_path, "a") as f:
        f.write(json.dumps({
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": "A",
            "location": "naver_api.py:8-9",
            "message": "Environment variables loaded",
            "data": {
                "NAVER_CLIENT_ID_exists": NAVER_CLIENT_ID is not None,
                "NAVER_CLIENT_ID_length": len(NAVER_CLIENT_ID) if NAVER_CLIENT_ID else 0,
                "NAVER_CLIENT_SECRET_exists": NAVER_CLIENT_SECRET is not None,
                "NAVER_CLIENT_SECRET_length": len(NAVER_CLIENT_SECRET) if NAVER_CLIENT_SECRET else 0,
            },
            "timestamp": int(__import__("time").time() * 1000)
        }) + "\n")
except Exception:
    pass
# #endregion


def search_shop(query: str, display: int = 10, start: int = 1, sort: str = "sim"):
    # #region agent log
    try:
        with open(log_path, "a") as f:
            f.write(json.dumps({
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "B",
                "location": "naver_api.py:35",
                "message": "search_shop called",
                "data": {"query": query, "display": display},
                "timestamp": int(__import__("time").time() * 1000)
            }) + "\n")
    except Exception:
        pass
    # #endregion
    
    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    
    # #region agent log
    try:
        with open(log_path, "a") as f:
            f.write(json.dumps({
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "C",
                "location": "naver_api.py:44",
                "message": "API request headers before request",
                "data": {
                    "client_id_is_none": NAVER_CLIENT_ID is None,
                    "client_secret_is_none": NAVER_CLIENT_SECRET is None,
                    "client_id_empty": NAVER_CLIENT_ID == "" if NAVER_CLIENT_ID else True,
                    "client_secret_empty": NAVER_CLIENT_SECRET == "" if NAVER_CLIENT_SECRET else True,
                },
                "timestamp": int(__import__("time").time() * 1000)
            }) + "\n")
    except Exception:
        pass
    # #endregion
    
    params = {"query": query, "display": display, "start": start, "sort": sort}

    response = requests.get(url, headers=headers, params=params)
    
    # #region agent log
    try:
        with open(log_path, "a") as f:
            f.write(json.dumps({
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": "D",
                "location": "naver_api.py:54",
                "message": "API response received",
                "data": {
                    "status_code": response.status_code,
                    "response_text": response.text[:200] if response.text else None,
                },
                "timestamp": int(__import__("time").time() * 1000)
            }) + "\n")
    except Exception:
        pass
    # #endregion
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
