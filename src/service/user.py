from sqlalchemy.orm import Session
from src.middleware.loggers import get_logger
from src.repository import user
from src.exceptions.custom_exception import ServiceError, RepositoryError
from pydantic import EmailStr
from src.model.user import User_Class, UserRole
from src.core.security import hash_password

logger = get_logger(__name__)

def create_user(payload, db : Session):
    try:
        has_admin = user.has_admin_user(db)
        assigned_role = UserRole.ADMIN if not has_admin else getattr(payload, "user_role", UserRole.USER)
        hashed_password = hash_password(payload.user_password)

        new_user = User_Class(
            user_name=payload.user_name,
            user_phone=payload.user_phone,
            user_email=payload.user_email,
            user_password=hashed_password,
            user_role=assigned_role,
        )

        return user.create_user(new_user, db)
    except RepositoryError as e:
        logger.error(f"Error creating User: {e}")
        raise ServiceError(f"Error creating User: {e}")
    
def get_user_by_email(email_id : EmailStr, db : Session):
    try:
        return user.get_user_by_email(email_id, db)
    except RepositoryError as e:
        logger.error(f"Error Fetching User: {e}")
        raise ServiceError(f"Error Fetching User: {e}")