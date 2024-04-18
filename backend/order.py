from backend.db_manager import DBManager
from datetime import datetime
from backend.product import *
class Order:
    def __init__(self, order_id, buyer_id, seller_id, item_id, status="paid", order_time=None, item_name=None):
        self.order_id = order_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.item_id = item_id
        self.status = status
        self.order_time = order_time if order_time else datetime.now().isoformat()
        self.item_name = item_name

def create_order(order_id, buyer_id, seller_id, item_id, status="=aid"):
    order_time = datetime.now().isoformat()  # ISO format: YYYY-MM-DDTHH:MM:SS.ffffff
    order_data = {
        "order_id": order_id,
        "buyer_id": buyer_id,
        "seller_id": seller_id,
        "item_id": item_id,
        "status": status,
        "order_time": order_time
    }
    db_manager = DBManager()
    db_manager.insert_order(order_data)
    return (True, "Order created successfully")

def get_order(order_id):
    db_manager = DBManager()
    order_data = db_manager.get(order_id, f"orders/{order_id}")
    if order_data:
        if order_data['item_id']:
            success, product = get_product(order_data['item_id'])
            if success:
                order_data['item_name'] = product.item_name
        if 'product_id' in order_data:
            del order_data['product_id']
        return (True, Order(**order_data))
    else:
        return (False, "Order not found")
