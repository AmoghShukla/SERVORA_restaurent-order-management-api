from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.service import user_service
from src.schema.user import UserCreate

router = APIRouter(prefix="/User", tags=["User"])

@router.post('/')
def create_user(payload : UserCreate, db : Session = Depends(get_db)):
    return user_service.create_user(payload, db)

@router.get('/{user_id}')
def get_user(user_id : int, db : Session = Depends(get_db)):
    return user_service.get_user(user_id, db)