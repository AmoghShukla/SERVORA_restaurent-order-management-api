from pydantic import BaseModel, Field
from typing import List


class CartItemAdd(BaseModel):
    item_id: int = Field(..., ge=1)
    quantity: int = Field(..., gt=0)


class CartItemResponse(BaseModel):
    item_id: int
    item_name: str
    item_price: int
    quantity: int
    total_price: int  # item_price * quantity

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    restaurent_id: int
    items: List[CartItemResponse]
    cart_total: int

    class Config:
        from_attributes = True
