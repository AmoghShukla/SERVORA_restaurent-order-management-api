from sqlalchemy.orm import Session
from src.exceptions.custom_exception import ServiceError, AlreadyExistsError

from src.repository.user import get_user_by_email, create_user, has_admin_user, make_owner as repo_make_owner
from src.model.user import User_Class, UserRole
from src.core.security import hash_password, verify_password, create_access_token

def SignUp(payload, db : Session):
    existing = get_user_by_email(payload.user_email, db)

    if existing:
        raise AlreadyExistsError(status_code=400, detail="User Already Exists!!")

    assigned_role = UserRole.ADMIN if not has_admin_user(db) else UserRole.USER
    
    hashed_password = hash_password(payload.user_password)

    user = User_Class(
        user_name = payload.user_name,
        user_phone = payload.user_phone,
        user_email = payload.user_email,
        user_password=hashed_password,
        user_role=assigned_role,
    )

    return create_user(user, db)

def login(payload, db : Session):
    user = get_user_by_email(payload.user_email, db)

    if not user:
        raise ServiceError(status_code=400, detail="User Does not exists!!")
    
    if not verify_password(payload.user_password, user.user_password):
        raise ServiceError(status_code=400, detail="Incorrect Password!!")
    
    role_value = user.user_role.value if hasattr(user.user_role, "value") else str(user.user_role)

    token = create_access_token({
        'sub' : str(user.user_id),
        'role' : role_value
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "message" : "Login Successful!!!!"
    }

def service_make_owner(user_id, db):
    return repo_make_owner(user_id, db)