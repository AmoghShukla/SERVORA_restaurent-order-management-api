from pydantic import BaseModel, Field


class RestaurentCreate(BaseModel):
    restaurent_name: str = Field(..., min_length=2, max_length=100)
    restaurent_address: str = Field(..., min_length=5, max_length=255)
    restaurent_phone: str = Field(..., min_length=7, max_length=12)
    restaurent_rating: int = Field(..., ge=0, le=5)


