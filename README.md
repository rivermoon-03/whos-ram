## Who's RAM?

램 어디까지 올라가는 거예요?

## 쓰는 법

### 1. 환경 변수 설정

루트 디렉토리에 `.env` 파일을 생성하고 다음 항목을 입력합니다.

```env
NAVER_CLIENT_ID=네이버_클라이언트_ID
NAVER_CLIENT_SECRET=네이버_클라이언트_SECRET
DATABASE_URL=supabase_연결_URI
API_KEY=사용할_보안_키 (기본값: your-secret-key-here)
```

### 2. 백엔드

```bash
cd backend
python -m venv venv
source venv/bin/activate      # 보통 이거.
source venv/bin/activate.fish # fish용.
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. 프론트엔드

```bash
cd frontend
npm install
npm run dev
```
