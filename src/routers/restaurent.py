from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.dependencies.auth import require_role
from src.model.restaurent import Restaurent_Class

router = APIRouter(prefix="/restaurent", tags=["Restaurent"])

@router.post("/")
def create_restaurent(payload: dict, db : Session = Depends(get_db), user=Depends(require_role(['ADMIN', 'RESTAURANT_OWNER']))):
    required_fields = [
        "Restaurent_name",
        "Restaurent_address",
        "Restaurent_phone",
        "Restaurent_rating",
    ]

    missing = [field for field in required_fields if field not in payload]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing fields: {', '.join(missing)}")

    restaurent = Restaurent_Class(
        Restaurent_name=payload["Restaurent_name"],
        Restaurent_address=payload["Restaurent_address"],
        Restaurent_phone=payload["Restaurent_phone"],
        Restaurent_rating=payload["Restaurent_rating"],
    )
    db.add(restaurent)
    db.commit()
    db.refresh(restaurent)
    return restaurent
