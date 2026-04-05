from sqlalchemy.orm import Session
from src.middleware.loggers import get_logger
from src.repository.order import create_order, get_orders_by_user

logger = get_logger(__name__)

def service_create_order(payload, db : Session, user):
    try:
        user_id = int(user["user_id"])
        return create_order(db, user_id)
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise Exception(f"Error creating order: {e}")
    
def service_get_all_orders(db : Session, user):
    try:
        user_id = user["user_id"]  
        return get_orders_by_user(db, user_id)
    except Exception as e:
        logger.error(f"Error fetching order: {e}")
        raise Exception(f"Error fetching order: {e}")
