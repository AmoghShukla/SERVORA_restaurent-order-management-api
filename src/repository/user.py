from src.middleware.loggers import get_logger
from sqlalchemy.orm import Session
from src.model.user import User_Class, UserRole
from sqlalchemy.exc import SQLAlchemyError
from src.exceptions.custom_exception import RepositoryError, ServiceError, NotFoundError 
from pydantic import EmailStr

logger = get_logger(__name__)

def get_user_by_email(email: EmailStr, db: Session):
    try:
        return db.query(User_Class).filter(User_Class.user_email == email).first()
    except SQLAlchemyError as e:
        raise RepositoryError(f"Failed to fetch user with email: {email}") from e


def has_admin_user(db: Session) -> bool:
    try:
        return db.query(User_Class).filter(User_Class.user_role == UserRole.ADMIN).first() is not None
    except SQLAlchemyError as e:
        raise RepositoryError("Failed to check admin presence") from e

def create_user(payload, db : Session):
    try:
        if isinstance(payload, User_Class):
            new_user = payload
            if new_user.user_role is None:
                new_user.user_role = UserRole.USER
        else:
            role = payload.user_role if hasattr(payload, "user_role") and payload.user_role is not None else UserRole.USER
            new_user = User_Class(
                user_name = payload.user_name,
                user_phone = payload.user_phone,
                user_email = payload.user_email,
                user_password=payload.user_password,
                user_role=role
            )
        logger.info(f"Creating user with payload: {payload}")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"User created successfully: {new_user}")
        return new_user
    except SQLAlchemyError as e:
        db.rollback()
        raise RepositoryError("Failed to Create User") from e

def get_user(user_id : int, db : Session):
    try:
        user = db.query(User_Class).filter(User_Class.user_id==user_id).first()
        if user:
            return user
    except Exception as e:
        print(e)
        return None


def make_owner(user_id: int, db: Session):
    try:
        user = db.query(User_Class).filter(User_Class.user_id == user_id).first()
        if not user:
            raise NotFoundError(status_code=404, detail="User not found")

        user.user_role = UserRole.RESTAURANT_OWNER
        db.commit()
        db.refresh(user)
        return user
    except NotFoundError:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise RepositoryError("Failed to promote user as restaurant owner") from e

