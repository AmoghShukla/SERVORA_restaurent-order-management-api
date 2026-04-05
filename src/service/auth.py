from sqlalchemy.orm import Session
from src.exceptions.custom_exception import ServiceError

from src.repository.user import get_user_by_email, create_user
from src.model.user import User_Class
from src.core.security import hash_password, verify_password, create_access_token

def SignUp(payload, db : Session):
    existing = get_user_by_email(payload.user_email, db)

    if existing:
        raise ServiceError(status_code=400, detail="User Already Exists!!")
    
    hashed_password = hash_password(payload.user_password)

    user = User_Class(
        user_name = payload.user_name,
        user_phone = payload.user_phone,
        user_email = payload.user_email,
        user_password=hashed_password
    )

    return create_user(user, db)

def login(payload, db : Session):
    user = get_user_by_email(payload.user_email, db)

    if not user:
        raise ServiceError(status_code=400, detail="User Does not exists!!")
    
    if not verify_password(payload.user_password, user.user_password):
        raise ServiceError(status_code=400, detail="Incorrect Password!!")
    
    token = create_access_token({
        'sub' : str(user.user_id),
        'role' : user.user_role.value
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }