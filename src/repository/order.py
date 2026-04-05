from src.middleware.loggers import get_logger
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.model.items import Items_Class
from src.model.order import Order_Class

logger = get_logger(__name__)

def create_order(payload, db: Session, user):
    try:
        data = payload.model_dump()
        item = db.query(Items_Class).filter(Items_Class.item_id == data["item_id"]).first()

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        total_amount = item.item_price * data["quantity"]

        new_order = Order_Class(
            user_id=getattr(user, "user_id", None),
            total_amount=total_amount,
            order_status="PENDING",
            payment_status="UNPAID"
        )
        logger.info(f"Creating order with payload: {payload}")
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        logger.info(f"Order created successfully: {new_order}")
        return new_order
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise Exception(f"Error creating order: {e}")