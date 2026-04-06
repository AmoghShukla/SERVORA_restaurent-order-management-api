from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.service import user
from src.schema.user import UserCreate
from pydantic import EmailStr

router = APIRouter(prefix="/User", tags=["User"])

@router.post('/')
def create_user(payload : UserCreate, db : Session = Depends(get_db)):
    return user.create_user(payload, db)

@router.get('/{user_id}')
def get_user(email_id :EmailStr , db : Session = Depends(get_db)):
    return user.get_user_by_email(email_id, db)