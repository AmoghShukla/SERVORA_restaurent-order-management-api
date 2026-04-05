from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.schema.order import OrderCreate, OrderResponse  
from src.database.session import get_db
from src.service.order import service_create_order, service_get_all_orders
from src.middleware.loggers import get_logger
from src.dependencies.auth import require_role

logger = get_logger(__name__)

router = APIRouter(prefix="/orders", tags=['orders'])

@router.post('/')
def create_order(payload : OrderCreate, db: Session = Depends(get_db), user=Depends(require_role(["USER"]))):
    try:
        return service_create_order(payload, db, user)
    except Exception as e:
        logger.error(f"Error creating order: {e} ")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/orders")
def get_all_orders(db : Session=Depends(get_db), user=Depends(require_role(["ADMIN"]))):
    try:
        return service_get_all_orders(db, user)
    except Exception as e:
        logger.error(f"Error creating order: {e} ")
        raise HTTPException(status_code=500, detail=str(e))