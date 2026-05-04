from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 0
    low_stock_threshold: int = 10
    category_id: int
    supplier_id: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    low_stock_threshold: Optional[int] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    low_stock_threshold: int
    category_id: int
    supplier_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LowStockResponse(BaseModel):
    id: int
    name: str
    quantity: int
    low_stock_threshold: int

    class Config:
        from_attributes = True
