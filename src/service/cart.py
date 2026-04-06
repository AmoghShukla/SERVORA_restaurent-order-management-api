from src.middleware.loggers import get_logger
from src.model.items import Items_Class
from src.model.menu import Menu_Class

logger = get_logger(__name__)

# In-memory cart storage: {user_id: {restaurent_id: {item_id: quantity, ...}, ...}}
_user_carts = {}


def add_to_cart(db, user_id: int, restaurent_id: int, item_id: int, quantity: int):
    """Add item to user's cart"""
    try:
        item = (
            db.query(Items_Class)
            .join(Menu_Class, Items_Class.menu_id == Menu_Class.cuisine_id)
            .filter(
                Items_Class.item_id == item_id,
                Menu_Class.restaurent_id == restaurent_id,
            )
            .first()
        )

        if not item:
            raise ValueError("Item not found for this restaurent")

        if not item.item_availability:
            raise ValueError("Item is currently unavailable")

        if user_id not in _user_carts:
            _user_carts[user_id] = {}
        
        if restaurent_id not in _user_carts[user_id]:
            _user_carts[user_id][restaurent_id] = {}
        
        cart = _user_carts[user_id][restaurent_id]
        
        if item_id in cart:
            cart[item_id] += quantity
        else:
            cart[item_id] = quantity
        
        logger.info(f"Added {quantity} of item {item_id} to user {user_id}'s cart")
        return {"message": "Item added to cart", "item_id": item_id, "quantity": cart[item_id]}
    except Exception as e:
        logger.error(f"Error adding to cart: {e}")
        raise


def remove_from_cart(user_id: int, restaurent_id: int, item_id: int):
    """Remove item from user's cart"""
    try:
        if user_id not in _user_carts or restaurent_id not in _user_carts[user_id]:
            raise ValueError("Cart is empty")
        
        cart = _user_carts[user_id][restaurent_id]
        
        if item_id not in cart:
            raise ValueError("Item not in cart")
        
        del cart[item_id]
        logger.info(f"Removed item {item_id} from user {user_id}'s cart")
        
        return {"message": "Item removed from cart"}
    except Exception as e:
        logger.error(f"Error removing from cart: {e}")
        raise


def get_cart(user_id: int, restaurent_id: int, db):
    """Get user's cart with item details"""
    try:
        from src.model.items import Items_Class
        
        if user_id not in _user_carts or restaurent_id not in _user_carts[user_id]:
            return {"restaurent_id": restaurent_id, "items": [], "cart_total": 0}
        
        cart = _user_carts[user_id][restaurent_id]
        items_response = []
        cart_total = 0
        
        for item_id, quantity in cart.items():
            item = db.query(Items_Class).filter(Items_Class.item_id == item_id).first()
            if item:
                total_price = item.item_price * quantity
                items_response.append({
                    "item_id": item_id,
                    "item_name": item.item_name,
                    "item_price": item.item_price,
                    "quantity": quantity,
                    "total_price": total_price
                })
                cart_total += total_price
        
        return {"restaurent_id": restaurent_id, "items": items_response, "cart_total": cart_total}
    except Exception as e:
        logger.error(f"Error fetching cart: {e}")
        raise


def clear_cart(user_id: int, restaurent_id: int):
    """Clear user's cart"""
    try:
        if user_id in _user_carts and restaurent_id in _user_carts[user_id]:
            _user_carts[user_id][restaurent_id].clear()
            logger.info(f"Cleared cart for user {user_id}")
        return {"message": "Cart cleared"}
    except Exception as e:
        logger.error(f"Error clearing cart: {e}")
        raise


def get_cart_items_for_order(user_id: int, restaurent_id: int) -> dict:
    """Get cart items formatted for order creation"""
    try:
        if user_id not in _user_carts or restaurent_id not in _user_carts[user_id]:
            raise ValueError("Cart is empty")
        
        cart = _user_carts[user_id][restaurent_id]
        items = []
        
        for item_id, quantity in cart.items():
            items.append({"item_id": item_id, "quantity": quantity})
        
        return items
    except Exception as e:
        logger.error(f"Error getting cart items: {e}")
        raise
