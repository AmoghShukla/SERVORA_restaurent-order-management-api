from pydantic import BaseModel, Field, model_validator

class OrderCreate(BaseModel):
    order_id  : int = Field(..., ge = 0)
    item_id   : int = Field(..., ge = 0)
    quantity  : int = Field(..., gt = 0)


class OrderResponse(BaseModel):
    order_id  : int = Field(..., ge = 0)
    user_id  : int = Field(..., ge = 0)
    items : list = Field(..., min_items = 1)
    order_status : str = Field(..., min_length = 1)
    total_price : float = Field(..., gt=0)
    created_at : str = Field(..., min_length = 1)