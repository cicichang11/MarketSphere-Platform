from backend.db_manager import DBManager
import uuid

class Product:
    def __init__(self, item_id, item_name, price, description, category, pictures, seller_id, inventory):
        self.item_id = item_id
        self.item_name = item_name
        self.price = price
        self.description = description
        self.category = category
        self.pictures = pictures
        self.seller_id = seller_id
        self.inventory = inventory

def create_product(item_id, item_name, price, description, category, pictures, seller_id, inventory):
    product_data = {
        "item_id": item_id,
        "item_name": item_name,
        "price": price,
        "description": description,
        "category": category,
        "pictures": pictures,
        "seller_id": seller_id,
        "inventory": inventory
    }
    db_manager = DBManager()
    db_manager.insert_product(product_data)
    return (True, "Product created successfully")

def get_product(item_id):
    db_manager = DBManager()
    product_data = db_manager.get(item_id, f"products/{item_id}")
    if product_data:
        # return (True, Product(**product_data))
        item_id = product_data.get("item_id")
        item_name = product_data.get("item_name")
        price = product_data.get("price")
        description = product_data.get("description")
        category = product_data.get("category")
        pictures = product_data.get("pictures", [])  # Provide a default value for 'pictures' if missing
        seller_id = product_data.get("seller_id")
        inventory = product_data.get("inventory")
        return (True, Product(item_id, item_name, price, description, category, pictures, seller_id, inventory))
    else:
        return (False, "Product not found")

def browse_products_by_category(category):
    db_manager = DBManager()
    products_data = db_manager.find_by_category(category)
    # products = [Product(**data) for data in products_data]
    products = []
    for data in products_data:
        item_id = data.get("item_id")
        item_name = data.get("item_name")
        price = data.get("price")
        description = data.get("description")
        category = data.get("category")
        pictures = data.get("pictures", [])  # Provide a default value for 'pictures' if missing
        seller_id = data.get("seller_id")
        inventory = data.get("inventory")
        product = Product(item_id, item_name, price, description, category, pictures, seller_id, inventory)
        products.append(product)
    return (True, products)
    

def search_products(search_term):
    db_manager = DBManager()
    products_data = db_manager.search_products(search_term)
    # products = [Product(**data) for data in products_data]
    products = []
    for data in products_data:
        item_id = data.get("item_id")
        item_name = data.get("item_name")
        price = data.get("price")
        description = data.get("description")
        category = data.get("category")
        pictures = data.get("pictures", [])  # Provide a default value for 'pictures' if missing
        seller_id = data.get("seller_id")
        inventory = data.get("inventory")
        product = Product(item_id, item_name, price, description, category, pictures, seller_id, inventory)
        products.append(product)
    return (True, products)