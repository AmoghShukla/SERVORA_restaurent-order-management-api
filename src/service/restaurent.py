from sqlalchemy.orm import Session
from src.middleware.loggers import get_logger
from src.repository.restaurent import create_restaurent as repo_create_restaurent
from src.model.restaurent import Restaurent_Class

logger = get_logger(__name__)


def service_create_restaurent(payload, db: Session, user):
    try:
        owner_id = int(user["user_id"])
        logger.info(f"Creating restaurent with owner_id: {owner_id}, payload: {payload}")
        return repo_create_restaurent(db, owner_id, payload)
    except Exception as e:
        logger.error(f"Error creating restaurent: {e}")
        raise
