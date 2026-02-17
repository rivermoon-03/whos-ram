# Railway Cron – 매일 KST 00:00 가격 업데이트

백엔드 `/api/update`를 호출해 램 가격을 매일 KST 00:00에 갱신하는 크론 서비스입니다.

## Railway 설정

1. **서비스 추가**  
   같은 프로젝트에 새 서비스를 만들고, **소스**에서 이 레포를 연결한 뒤 **Root Directory**를 `cron`으로 지정합니다.

2. **Cron Schedule**  
   서비스 **Settings** → **Cron Schedule**에 다음을 입력합니다.  
   (Railway는 UTC 기준이므로, KST 00:00 = UTC 15:00)

   ```text
   0 15 * * *
   ```

3. **환경 변수**  
   서비스 또는 프로젝트 변수로 다음을 설정합니다.

   | 변수 | 설명 |
   |------|------|
   | `BACKEND_URL` | 백엔드 주소 (예: `https://your-backend.railway.app`) |
   | `API_KEY` 또는 `VITE_API_KEY` | 백엔드와 동일한 API 키 |

4. **동작**  
   매일 UTC 15:00(KST 00:00)에 `python run.py`가 실행되고, `BACKEND_URL/api/update`로 POST 요청을 보낸 뒤 종료됩니다.

## 로컬에서 테스트

```bash
cd cron
pip install -r requirements.txt
export BACKEND_URL=https://your-backend.railway.app
export API_KEY=your-api-key
python run.py
```
