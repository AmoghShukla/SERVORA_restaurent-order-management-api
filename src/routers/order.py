from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.schema.order import OrderCreate, OrderFromCartCreate, OrderResponse
from src.database.session import get_db
from src.service.order import (
    service_create_order,
    service_create_order_from_cart,
    service_get_all_orders,
    service_get_order_history,
)
from src.middleware.loggers import get_logger
from src.dependencies.auth import require_role

logger = get_logger(__name__)

router = APIRouter(prefix="/orders", tags=['Orders'])

@router.post('/')
def create_order(payload : OrderCreate, db: Session = Depends(get_db), user=Depends(require_role(["USER", "ADMIN", "RESTAURANT_OWNER"]))):
    try:
        return service_create_order(payload, db, user)
    except Exception as e:
        logger.error(f"Error creating order: {e} ")
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/from-cart')
def create_order_from_cart(payload: OrderFromCartCreate, db: Session = Depends(get_db), user=Depends(require_role(["USER", "ADMIN", "RESTAURANT_OWNER"]))):
    try:
        return service_create_order_from_cart(payload, db, user)
    except Exception as e:
        logger.error(f"Error creating order from cart: {e} ")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/")
def get_all_orders(db : Session=Depends(get_db), user=Depends(require_role(["USER", "ADMIN", "RESTAURANT_OWNER"]))):
    try:
        return service_get_all_orders(db, user)
    except Exception as e:
        logger.error(f"Error creating order: {e} ")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
def get_order_history(db: Session = Depends(get_db), user=Depends(require_role(["USER", "ADMIN", "RESTAURANT_OWNER"]))):
    try:
        return service_get_order_history(db, user)
    except Exception as e:
        logger.error(f"Error fetching order history: {e} ")
        raise HTTPException(status_code=500, detail=str(e))