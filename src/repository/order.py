from src.middleware.loggers import get_logger
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.model.items import Items_Class
from src.model.order import Order_Class
from src.model.OrderItems import OrderItems_Class

logger = get_logger(__name__)

def create_order(db: Session, user_id: int):
    order = Order_Class(
        user_id=user_id,
        order_status="PENDING",
        payment_status="UNPAID",
        total_amount=0
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

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
