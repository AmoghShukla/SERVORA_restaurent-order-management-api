from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from src.schema.user import UserCreate, UserLogin, Token
from src.database.session import get_db
from src.service.auth import SignUp, login
from src.dependencies.auth import require_role
from src.service.auth import service_make_owner


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def Signup_user(payload : UserCreate, db : Session = Depends(get_db)):
    return SignUp(payload, db)

@router.post("/login", response_model=Token)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    return login(payload, db)

@router.patch("/users/{user_id}/make-owner")
def make_owner(
    user_id: int,
    db: Session = Depends(get_db),
    admin = Depends(require_role(['ADMIN']))
):
    return service_make_owner(user_id, db)
