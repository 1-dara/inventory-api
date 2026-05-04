from pydantic import BaseModel
from datetime import datetime


class SaleCreate(BaseModel):
    product_id: int
    quantity: int


class SaleResponse(BaseModel):
    id: int
    product_id: int
    staff_id: int
    quantity: int
    unit_price: float
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True
