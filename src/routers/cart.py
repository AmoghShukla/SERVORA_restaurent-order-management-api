from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.dependencies.auth import require_role
from src.schema.cart import CartItemAdd
from src.service.cart import add_to_cart, clear_cart, get_cart, remove_from_cart

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/{restaurent_id}/items")
def add_item_to_cart(
	restaurent_id: int,
	payload: CartItemAdd,
	db: Session = Depends(get_db),
	user=Depends(require_role(["USER", "ADMIN", "RESTAURANT_OWNER"])),
):
	try:
		user_id = int(user["user_id"])
		return add_to_cart(db, user_id, restaurent_id, payload.item_id, payload.quantity)
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.get("/{restaurent_id}")
def get_user_cart(
	restaurent_id: int,
	db: Session = Depends(get_db),
	user=Depends(require_role(["USER", "ADMIN", "RESTAURANT_OWNER"])),
):
	try:
		user_id = int(user["user_id"])
		return get_cart(user_id, restaurent_id, db)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{restaurent_id}/items/{item_id}")
def delete_item_from_cart(
	restaurent_id: int,
	item_id: int,
	user=Depends(require_role(["USER", "ADMIN", "RESTAURANT_OWNER"])),
):
	try:
		user_id = int(user["user_id"])
		return remove_from_cart(user_id, restaurent_id, item_id)
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{restaurent_id}")
def clear_user_cart(
	restaurent_id: int,
	user=Depends(require_role(["USER", "ADMIN", "RESTAURANT_OWNER"])),
):
	try:
		user_id = int(user["user_id"])
		return clear_cart(user_id, restaurent_id)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
