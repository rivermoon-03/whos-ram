from pydantic import BaseModel
from typing import List
from datetime import datetime


class ProductBase(BaseModel):
    id: str
    name: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    created_at: datetime

    class Config:
        from_attributes = True


class PriceHistory(BaseModel):
    id: int
    product_id: str
    price: int
    timestamp: datetime

    class Config:
        from_attributes = True


class ProductWithHistory(Product):
    price_history: List[PriceHistory] = []
