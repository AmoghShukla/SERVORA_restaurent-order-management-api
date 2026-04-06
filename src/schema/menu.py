from pydantic import BaseModel, Field


class MenuCreate(BaseModel):
    cuisine_name: str = Field(..., min_length=2, max_length=100)
