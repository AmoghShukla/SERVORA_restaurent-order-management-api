from sqlalchemy.orm import Session
from src.middleware.loggers import get_logger
from src.repository import order_repository

logger = get_logger(__name__)

def service_create_order(payload, db : Session, user):
    try:
        return order_repository.create_order(payload, db, user)
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise Exception(f"Error creating order: {e}")