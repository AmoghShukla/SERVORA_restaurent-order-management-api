from sqlalchemy.orm import Session
from src.middleware.loggers import get_logger
from src.repository import user
from src.exceptions.custom_exception import ServiceError, RepositoryError
from pydantic import EmailStr

logger = get_logger(__name__)

def create_user(payload, db : Session):
    try:
        return user.create_user(payload, db)
    except RepositoryError as e:
        logger.error(f"Error creating User: {e}")
        raise ServiceError(f"Error creating User: {e}")
    
def get_user_by_email(email_id : EmailStr, db : Session):
    try:
        return user.get_user_by_email(email_id, db)
    except RepositoryError as e:
        logger.error(f"Error Fetching User: {e}")
        raise ServiceError(f"Error Fetching User: {e}")