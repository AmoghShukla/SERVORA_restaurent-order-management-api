from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.schema.order import OrderCreate, OrderResponse  
from src.database.session import get_db
from src.service import order
from src.utils.loggers import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/orders", tags=['orders'])

@router.post('/', response_model=OrderResponse)
def create_order(payload : OrderCreate, db: Session = Depends(get_db)):
    try:
        return order.service_create_order(payload, db)
    except HTTPException as e:
        raise f"{e}"