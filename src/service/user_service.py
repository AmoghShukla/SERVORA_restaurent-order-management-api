from sqlalchemy.orm import Session
from src.middleware.loggers import get_logger
from repository import user

logger = get_logger(__name__)

def create_user(payload, db : Session):
    try:
        return user.create_user(payload, db)
    except Exception as e:
        logger.error(f"Error creating User: {e}")
        raise Exception(f"Error creating User: {e}")
    
def get_user(user_id : int, db : Session):
    try:
        return user.get_user(user_id, db)
    except Exception as e:
        logger.error(f"Error Fetching User: {e}")
        raise Exception(f"Error Fetching User: {e}")