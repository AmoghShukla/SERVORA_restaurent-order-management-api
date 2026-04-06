
from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    item_name: str = Field(..., min_length=2, max_length=100)
    item_price: int = Field(..., ge=0)
    item_rating: int = Field(..., ge=0, le=5)
    item_availability: bool = True
