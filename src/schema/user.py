from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    user_name: str = Field(..., min_length=2, max_length=50)
    user_email: EmailStr
    user_password : str = Field(..., min_length=5)
    user_phone: str = Field(..., min_length=10, max_length=15)

class UserLogin(BaseModel):
    user_email : EmailStr
    user_password : str = Field(..., min_length=5)

class Token(BaseModel):
    access_token : str
    token_type : str = "bearer"