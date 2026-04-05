from pydantic import BaseModel, Field
from typing import List


class OrderItemCreate(BaseModel):
    item_id: int = Field(..., ge=1)
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]   
    address: str = Field(..., min_length=1)

class OrderItemResponse(BaseModel):
    item_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    order_id: int
    total_price: float
    order_status: str
    address: str
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True