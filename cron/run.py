#!/usr/bin/env python3
"""
Railway Cron: KST 00:00(UTC 15:00)에 백엔드 /api/update 를 호출 후 종료.
환경변수: BACKEND_URL, API_KEY (또는 VITE_API_KEY)
"""
import os
import sys

try:
    import requests
except ImportError:
    print("requests 미설치. pip install requests", file=sys.stderr)
    sys.exit(1)

def main():
    base = (os.getenv("BACKEND_URL") or "").rstrip("/")
    api_key = (os.getenv("API_KEY") or os.getenv("VITE_API_KEY") or "").strip()
    if not base:
        print("BACKEND_URL 환경변수가 필요합니다.", file=sys.stderr)
        sys.exit(1)
    if not api_key:
        print("API_KEY 또는 VITE_API_KEY 환경변수가 필요합니다.", file=sys.stderr)
        sys.exit(1)

    url = f"{base}/api/update"
    headers = {"X-API-KEY": api_key}
    try:
        r = requests.post(url, headers=headers, timeout=120)
        r.raise_for_status()
        print(r.json())
    except requests.RequestException as e:
        print(f"요청 실패: {e}", file=sys.stderr)
        if hasattr(e, "response") and e.response is not None:
            print(e.response.text, file=sys.stderr)
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
