from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Product(Base):  # 램 8, 16, 32GB가 들어갈거임.
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)  # 네이버 상품 ID
    name = Column(String, index=True)  # 이름
    created_at = Column(DateTime, default=datetime.utcnow)

    price_history = relationship("PriceHistory", back_populates="product")
    # 1대N으로 가격 히스토리랑 연결.


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, ForeignKey("products.id"))  # FK로 연결.
    price = Column(Integer)  # 가격
    timestamp = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="price_history")
