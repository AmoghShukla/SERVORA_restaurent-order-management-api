from src.middleware.loggers import get_logger
from sqlalchemy.orm import Session
from src.model.user import User_Class
from fastapi import HTTPException

logger = get_logger(__name__)

def create_user(payload, db : Session):
    try:
        new_user = User_Class(
            user_name = payload.user_name,
            user_phone = payload.user_phone,
            user_email = payload.user_email
        )
        logger.info(f"Creating user with payload: {payload}")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"Order created successfully: {new_user}")
        return new_user
    except Exception as e:
        
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def get_user(user_id : int, db : Session):
    try:
        user = db.query(User_Class).filter(User_Class.user_id==user_id).first()
        if user:
            return user
    except Exception as e:
        print(e)
        return None

