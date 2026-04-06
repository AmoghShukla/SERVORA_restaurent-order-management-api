from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.dependencies.auth import require_role
from src.schema.menu import MenuCreate
from src.service.menu import service_create_menu, service_get_restaurent_menu

router = APIRouter(prefix="/menu", tags=["Menu"])


@router.post("/{restaurent_id}")
def create_menu(restaurent_id: int, payload: MenuCreate, db: Session = Depends(get_db), user=Depends(require_role(['ADMIN', 'RESTAURANT_OWNER']))):
    try:
        return service_create_menu(restaurent_id, payload, db, user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{restaurent_id}")
def get_restaurent_menu(restaurent_id: int, db: Session = Depends(get_db)):
    try:
        return service_get_restaurent_menu(restaurent_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
