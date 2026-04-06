from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.middleware.loggers import get_logger

from src.exceptions.custom_exception import RepositoryError, NotFoundError
from src.model.restaurent import Restaurent_Class
from src.model.menu import Menu_Class
from src.model.items import Items_Class

logger = get_logger(__name__)


def create_restaurent(db: Session, owner_id: int, payload):
    try:
        restaurent = Restaurent_Class(
            owner_id=owner_id,
            Restaurent_name=payload.restaurent_name,
            Restaurent_address=payload.restaurent_address,
            Restaurent_phone=payload.restaurent_phone,
            Restaurent_rating=payload.restaurent_rating,
        )
        db.add(restaurent)
        db.commit()
        db.refresh(restaurent)
        return restaurent
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating restaurent: {e}")
        raise RepositoryError("Failed to create restaurent") from e


def create_menu(db: Session, restaurent_id: int, payload):
    try:
        restaurent = db.query(Restaurent_Class).filter(Restaurent_Class.Restaurent_id == restaurent_id).first()
        if not restaurent:
            raise NotFoundError(status_code=404, detail="Restaurent not found")

        menu = Menu_Class(
            restaurent_id=restaurent_id,
            cuisine_name=payload.cuisine_name,
        )
        db.add(menu)
        db.commit()
        db.refresh(menu)
        return menu
    except NotFoundError:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise RepositoryError("Failed to create menu") from e


def create_item(db: Session, menu_id: int, payload):
    try:
        menu = db.query(Menu_Class).filter(Menu_Class.cuisine_id == menu_id).first()
        if not menu:
            raise NotFoundError(status_code=404, detail="Menu not found")

        item = Items_Class(
            menu_id=menu_id,
            item_name=payload.item_name,
            item_price=payload.item_price,
            item_rating=payload.item_rating,
            item_availability=payload.item_availability,
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except NotFoundError:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise RepositoryError("Failed to create item") from e


def get_restaurent_menu(db: Session, restaurent_id: int):
    return (
        db.query(Menu_Class)
        .filter(Menu_Class.restaurent_id == restaurent_id)
        .all()
    )


def get_menu_items(db: Session, menu_id: int):
    return (
        db.query(Items_Class)
        .filter(Items_Class.menu_id == menu_id)
        .all()
    )
