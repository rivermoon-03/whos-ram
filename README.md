# Whos RAM - 실시간 삼성 RAM 가격 추적기

네이버 쇼핑 API를 활용하여 삼성전자 DDR5 RAM의 가격 변동을 실시간으로 추적하고 시각화하는 웹 애플리케이션입니다.

## 🚀 주요 기능

- **실시간 가격 추적**: 네이버 쇼핑 API를 통해 삼성전자 DDR5 16GB, 32GB 모델의 최저가를 주기적으로 확인합니다.
- **데이터 시각화**: 수집된 가격 데이터를 Highcharts를 사용하여 직관적인 그래프로 보여줍니다.
- **보안 API**: API Key를 사용하여 허가되지 않은 접근으로부터 데이터를 보호합니다.
- **Supabase 연동**: 클라우드 PostgreSQL(Supabase)을 사용하여 어디서든 안전하게 데이터를 관리합니다.

## 🛠 기술 스택

### Backend

- **Framework**: FastAPI
- **Database**: PostgreSQL (via Supabase)
- **ORM**: SQLAlchemy
- **Data Fetching**: Requests (Naver Shopping API)

### Frontend

- **Framework**: React (Vite)
- **Styling**: Vanilla CSS
- **Visualization**: Highcharts

## ⚙️ 설치 및 시작하기

### 1. 환경 변수 설정

루트 디렉토리에 `.env` 파일을 생성하고 다음 항목을 입력합니다.

```env
NAVER_CLIENT_ID=네이버_클라이언트_ID
NAVER_CLIENT_SECRET=네이버_클라이언트_SECRET
DATABASE_URL=supabase_연결_URI
API_KEY=사용할_보안_키 (기본값: your-secret-key-here)
```

### 2. 백엔드 실행

```bash
cd backend
python -m venv venv
source venv/bin/activate      # 보통 이거.
source venv/bin/activate.fish # fish용.
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

### 4. .env 파일

```
NAVER_CLIENT_ID=네이버_클라이언트_ID
NAVER_CLIENT_SECRET=네이버_클라이언트_SECRET
DATABASE_URL=supabase_연결_URI
API_KEY=사용할_보안_키
```
