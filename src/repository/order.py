from src.middleware.loggers import get_logger
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from src.exceptions.custom_exception import RepositoryError, NotFoundError
from src.model.items import Items_Class
from src.model.order import Order_Class
from src.model.OrderItems import OrderItems_Class
from src.model.menu import Menu_Class
from src.model.restaurent import Restaurent_Class

logger = get_logger(__name__)

def create_order(db: Session, user_id: int, payload):
    try:
        restaurent = db.query(Restaurent_Class).filter(Restaurent_Class.Restaurent_id == payload.restaurent_id).first()
        if not restaurent:
            raise NotFoundError(status_code=404, detail="Restaurent not found")

        order = Order_Class(
            user_id=user_id,
            restaurent_id=payload.restaurent_id,
            address=payload.address,
            order_status="PENDING",
            payment_status="UNPAID",
            total_amount=0,
        )
        db.add(order)
        db.flush()

        total_amount = 0
        order_items = []

        for item_request in payload.items:
            item = (
                db.query(Items_Class)
                .join(Menu_Class, Items_Class.menu_id == Menu_Class.cuisine_id)
                .filter(
                    Items_Class.item_id == item_request.item_id,
                    Menu_Class.restaurent_id == payload.restaurent_id,
                )
                .first()
            )

            if not item:
                raise NotFoundError(status_code=404, detail=f"Item {item_request.item_id} not found for this restaurent")

            if not item.item_availability:
                raise RepositoryError(f"Item {item.item_name} is currently unavailable")

            line_price = item.item_price * item_request.quantity
            total_amount += line_price

            order_item = OrderItems_Class(
                order_id=order.order_id,
                item_id=item.item_id,
                item_quantity=item_request.quantity,
                price=line_price,
            )
            db.add(order_item)
            order_items.append(order_item)

        order.total_amount = total_amount
        db.commit()
        db.refresh(order)
        return {
            "order": order,
            "items": order_items,
            "total_amount": total_amount,
        }
    except (NotFoundError, RepositoryError):
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise RepositoryError("Failed to create order") from e

def add_order_items(db : Session, order_id : int, items : list):
    order_items = []

    for item in items:
        order_item = OrderItems_Class(
            order_id=order_id,
            item_id=item["item_id"],
            item_quantity=item["quantity"],
            price=item["price"]
        )
        db.add(order_item)
        order_items.append(order_item)
    
    db.commit()
    return order_items

def update_order_total(db : Session, order, total):
    order.total_amount = total
    db.commit()
    db.refresh(order)
    return order

def get_orders_by_user(db: Session, user_id : int):
    return db.query(Order_Class).filter(Order_Class.user_id == user_id).all()

def get_order_history_by_user(db: Session, user_id: int):
    orders = (
        db.query(Order_Class)
        .options(
            joinedload(Order_Class.order_items).joinedload(OrderItems_Class.item),
            joinedload(Order_Class.restaurent),
        )
        .filter(Order_Class.user_id == user_id)
        .order_by(Order_Class.created_at.desc())
        .all()
    )

    history = []
    for order in orders:
        items = []
        for order_item in order.order_items:
            item_name = None
            if order_item.item is not None:
                item_name = order_item.item.item_name

            items.append(
                {
                    "item_id": order_item.item_id,
                    "item_name": item_name,
                    "quantity": order_item.item_quantity,
                    "line_total": order_item.price,
                }
            )

        restaurent_name = None
        if order.restaurent is not None:
            restaurent_name = order.restaurent.Restaurent_name

        history.append(
            {
                "order_id": order.order_id,
                "restaurent_id": order.restaurent_id,
                "restaurent_name": restaurent_name,
                "address": order.address,
                "order_status": order.order_status,
                "payment_status": order.payment_status,
                "total_amount": order.total_amount,
                "created_at": order.created_at,
                "items": items,
            }
        )

    return history
