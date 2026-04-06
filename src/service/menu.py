from sqlalchemy.orm import Session
from src.middleware.loggers import get_logger
from src.repository.restaurent import create_menu as repo_create_menu, get_restaurent_menu as repo_get_restaurent_menu
from src.model.restaurent import Restaurent_Class
from src.model.menu import Menu_Class

logger = get_logger(__name__)


def _is_admin(user):
    return str(user.get("role", "")).upper() == "ADMIN"


def _ensure_restaurent_access(db: Session, restaurent_id: int, user):
    if _is_admin(user):
        return

    restaurent = db.query(Restaurent_Class).filter(Restaurent_Class.Restaurent_id == restaurent_id).first()
    if not restaurent:
        raise ValueError("Restaurent not found")

    if int(user["user_id"]) != restaurent.owner_id:
        raise PermissionError("You can manage only your own restaurent")


def service_create_menu(restaurent_id: int, payload, db: Session, user):
    try:
        _ensure_restaurent_access(db, restaurent_id, user)
        return repo_create_menu(db, restaurent_id, payload)
    except Exception as e:
        logger.error(f"Error creating menu: {e}")
        raise


def service_get_restaurent_menu(restaurent_id: int, db: Session):
    try:
        return repo_get_restaurent_menu(db, restaurent_id)
    except Exception as e:
        logger.error(f"Error fetching restaurent menu: {e}")
        raise
