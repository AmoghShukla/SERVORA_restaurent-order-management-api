from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from model.order import OrderCreate, OrderResponse  
from db.session import get_db

router = APIRouter(prefix="/orders", tags=['orders'])

@router.post('/', response_model=OrderResponse)
def create_order(payload : OrderCreate, db: Session = Depends(get_db)):
    try:
        return service.create_order(db)
    except HTTPException as e:
        raise f"{e}"