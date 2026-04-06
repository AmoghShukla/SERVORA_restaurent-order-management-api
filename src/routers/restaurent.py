from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.dependencies.auth import require_role
from src.schema.restaurent import RestaurentCreate
from src.service.restaurent import service_create_restaurent

router = APIRouter(prefix="/restaurent", tags=["Restaurent"])


@router.post("/")
def create_restaurent(payload: RestaurentCreate, db: Session = Depends(get_db), user=Depends(require_role(['ADMIN', 'RESTAURANT_OWNER']))):
    try:
        return service_create_restaurent(payload, db, user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
