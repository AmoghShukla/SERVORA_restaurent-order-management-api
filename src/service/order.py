from sqlalchemy.orm import Session
from src.utils.loggers import get_logger
from src.repository import order

logger = get_logger(__name__)

def service_create_order(payload, db : Session):
    try:
        return order.create_order(payload, db)
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise Exception(f"Error creating order: {e}")