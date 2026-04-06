from sqlalchemy.orm import Session
from src.middleware.loggers import get_logger
from src.repository.order import create_order, get_order_history_by_user, get_orders_by_user
from src.service.cart import get_cart_items_for_order, clear_cart

logger = get_logger(__name__)

def service_create_order(payload, db : Session, user):
    try:
        user_id = int(user["user_id"])
        return create_order(db, user_id, payload)
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise Exception(f"Error creating order: {e}")


def service_create_order_from_cart(payload, db: Session, user):
    try:
        user_id = int(user["user_id"])
        cart_items = get_cart_items_for_order(user_id, payload.restaurent_id)

        order_payload = type("OrderPayload", (), {
            "restaurent_id": payload.restaurent_id,
            "address": payload.address,
            "items": [
                type("OrderItemPayload", (), item)
                for item in cart_items
            ],
        })

        result = create_order(db, user_id, order_payload)
        clear_cart(user_id, payload.restaurent_id)
        return result
    except Exception as e:
        logger.error(f"Error creating order from cart: {e}")
        raise Exception(f"Error creating order from cart: {e}")
    
def service_get_all_orders(db : Session, user):
    try:
        user_id = int(user["user_id"])
        return get_orders_by_user(db, user_id)
    except Exception as e:
        logger.error(f"Error fetching order: {e}")
        raise Exception(f"Error fetching order: {e}")


def service_get_order_history(db: Session, user):
    try:
        user_id = int(user["user_id"])
        return get_order_history_by_user(db, user_id)
    except Exception as e:
        logger.error(f"Error fetching order history: {e}")
        raise Exception(f"Error fetching order history: {e}")
