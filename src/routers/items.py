from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.dependencies.auth import require_role
from src.schema.items import ItemCreate
from src.service.items import service_create_item, service_get_menu_items

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/{menu_id}")
def create_item(menu_id: int, payload: ItemCreate, db: Session = Depends(get_db), user=Depends(require_role(['ADMIN', 'RESTAURANT_OWNER']))):
    try:
        return service_create_item(menu_id, payload, db, user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{menu_id}")
def get_menu_items(menu_id: int, db: Session = Depends(get_db)):
    try:
        return service_get_menu_items(menu_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
