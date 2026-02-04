import os
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import database
import naver_api
import schemas
from database import engine, get_db
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv, find_dotenv

# .env 찾기
load_dotenv(find_dotenv(), override=True)

# DB 스키마
models.Base.metadata.create_all(bind=engine)

# API 키
API_KEY_NAME = "X-API-KEY"
API_KEY = (
    os.getenv("VITE_API_KEY") or os.getenv("API_KEY") or "your-secret-key-here"
).strip()
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


# API 키 검증
def verify_api_key(x_api_key: str = Depends(api_key_header)):
    if not x_api_key or x_api_key.strip() != API_KEY:
        raise HTTPException(
            status_code=403, detail="허가되지 않은 접근입니다. API 키를 확인하세요."
        )
    return x_api_key


app = FastAPI(
    title="Who's RAM?",
    description="램꽈배기",
    version="1.0.0",
)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "*.vercel.app",  # Vercel 배포 도메인 허용
    os.getenv("FRONTEND_URL"),  # Railway 배포 시 Vercel 도메인 명시
    os.getenv("VITE_API_URL"),  # 혹시 모를 추가 도메인
]

origins = [origin for origin in origins if origin]  # None 제거

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vercel용 설정임.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_router = APIRouter(prefix="/api")


@app.get("/")
@api_router.get("/")
def read_root():
    return {"조선의 궁궐에 당도한 것을 환영하오": "낮선이여."}


@app.on_event("startup")
def startup_event():
    # 앱 시작 시 DB 초기화 및 상품 시딩
    seed_products()


@api_router.get("/products", response_model=List[schemas.ProductWithHistory])
def read_products(db: Session = Depends(get_db), _=Depends(verify_api_key)):
    # 램값들 조회
    return db.query(models.Product).all()


def seed_products():
    # 삼성 시금치 램들
    ram = [
        {"id": "52204538636", "name": "삼성전자 DDR5 PC5-44800 8GB"},
        {"id": "52204540637", "name": "삼성전자 DDR5 PC5-44800 16GB"},
        {"id": "52204543625", "name": "삼성전자 DDR5 PC5-44800 32GB"},
    ]

    # 병렬 처리를 위한 작업자 함수
    def process_product(t):
        # 각 스레드마다 새로운 DB 세션 생성
        local_db = database.SessionLocal()
        try:
            exists = (
                local_db.query(models.Product)
                .filter(models.Product.id == t["id"])
                .first()
            )
            if not exists:
                product = models.Product(id=t["id"], name=t["name"])
                local_db.add(product)
                local_db.commit()
                # 가격 업데이트도 바로 수행
                update_price_single(local_db, product)
        except Exception as e:
            print(f"Error processing {t['name']}: {e}")
        finally:
            local_db.close()

    # 메인 스레드에서는 이미 데이터가 있는지 가볍게 체크할 수도 있지만,
    # Vercel 콜드 스타트 시에는 비어있을 확률이 높으므로 바로 병렬 실행
    # 단, 요청이 겹칠 경우를 대비해 DB 락/경합이 있을 수 있으나 SQLite/Postgres 기본 트랜잭션으로 처리

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(process_product, ram)


def update_price_single(db: Session, product: models.Product):
    # 네이버 쇼핑 API로 램 가격 업데이트
    try:
        result = naver_api.search_shop(product.name, display=5)
        items = result.get("items", [])

        target_item = None
        for item in items:
            if item["productId"] == product.id:
                target_item = item
                break

        if target_item:
            price = int(target_item["lprice"])
            price_history = models.PriceHistory(product_id=product.id, price=price)
            db.add(price_history)
            db.commit()
            print(f"✅ {product.name}: {price}원 업데이트 완료")
            return {"success": True, "product": product.name, "price": price}
        else:
            error_msg = f"❌ 검색 실패 {product.id}: {product.name} - API 결과에서 상품을 찾을 수 없습니다"
            print(error_msg)
            return {"success": False, "product": product.name, "error": "상품을 찾을 수 없습니다"}

    except Exception as e:
        error_msg = f"❌ Error updating price for {product.name}: {str(e)}"
        print(error_msg)
        db.rollback()  # 에러 발생 시 롤백
        return {"success": False, "product": product.name, "error": str(e)}


@api_router.post("/update")
def update_prices(
    db: Session = Depends(get_db),
    _=Depends(verify_api_key),
):
    """
    모든 제품의 가격을 업데이트합니다.
    BackgroundTasks 대신 동기적으로 실행하여 Railway 환경에서도 안정적으로 작동합니다.
    """
    products = db.query(models.Product).all()
    
    if not products:
        return {"message": "업데이트할 제품이 없습니다.", "results": []}
    
    results = []
    success_count = 0
    fail_count = 0
    
    for product in products:
        print(f"🔄 업데이트 중: {product.name} (ID: {product.id})")
        result = update_price_single(db, product)
        results.append(result)
        
        if result.get("success"):
            success_count += 1
        else:
            fail_count += 1
    
    return {
        "message": f"업데이트 완료. 성공: {success_count}, 실패: {fail_count}",
        "success_count": success_count,
        "fail_count": fail_count,
        "results": results
    }


app.include_router(api_router)
