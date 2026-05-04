from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StockMovementCreate(BaseModel):
    product_id: int
    movement_type: str  # "in" or "out"
    quantity: int
    reason: Optional[str] = None


class StockMovementResponse(BaseModel):
    id: int
    product_id: int
    movement_type: str
    quantity: int
    reason: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
