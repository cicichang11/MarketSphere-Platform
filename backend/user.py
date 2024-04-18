import hashlib
from backend.order import get_order
from backend.product import get_product
from backend.db_manager import DBManager
import uuid

# Global variable to keep track of the currently signed-in user
current_user = None

def get_current_user():
    global current_user
    return current_user

def get_current_user_role():
    global current_user
    return current_user.user_role if current_user else None

class User:
    def __init__(self, email, user_name, first_name, last_name, sha_hashed_password, user_role, order_history=None, product_listings=None, cart=None):
        self.email = email
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.sha_hashed_password = sha_hashed_password
        self.user_role = user_role
        self.order_history = order_history
        self.product_listings = product_listings
        self.cart = cart

    def my_orders(self):
        return (True, self.order_history)
    
class Buyer(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.cart is None:
            self.cart = {"cart": ["dummy"]}
        if self.order_history is None:
            self.order_history = {"order_history": ["dummy"]}
    
    def get_order_history(self):
        db_manager = DBManager()
        order_ids = self.order_history["order_history"]
        orders = []
        for order_id in order_ids:
            if order_id != "dummy":
                success, order = get_order(order_id)
                if success:
                    orders.append(order)
                else:
                    print(f"Order not found for order ID: {order_id}")
        return (True, orders)
    
    def my_cart(self):
        return (True, self.cart)

    def add_to_cart(self, item_id):
        self.cart["cart"].append(item_id)
        db_manager = DBManager()
        db_manager.patch(self.email, f"users/{self.email.replace('.', ',')}/cart", self.cart)
        return (True, "Product added to cart")

    def remove_from_cart(self, item_id):
        if item_id in self.cart["cart"]:
            self.cart["cart"].remove(item_id)
            db_manager = DBManager()
            db_manager.patch(self.email, f"users/{self.email.replace('.', ',')}/cart", self.cart)
            return (True, "Product removed from cart")
        else:
            return (False, "Product not found in cart")

    def make_order(self, item_id):
        db_manager = DBManager()
        
        # Retrieve product to get seller_id
        
        successful, product = get_product(item_id)
        print(product)
        if not product or int(product.inventory) < 1 or item_id is None:
            return (False, "Product not found, out of stock, or item_id is missing")
        
        product.inventory = int(product.inventory)-1  # Decrement inventory
        db_manager.update_product_inventory(item_id, product.inventory) 
        
        # Generate a unique order ID
        order_id = str(uuid.uuid4())
        order_data = {
            "order_id": order_id,
            "buyer_id": self.email,
            "seller_id": product.seller_id,
            "item_id": item_id,
            "status": "paid"
        }
        
        # Insert the new order into the database
        db_manager.insert_order(order_data)
        
        # Update Buyer's order history
        self.order_history["order_history"].append(order_id)
        db_manager.patch(self.email, f"users/{self.email.replace('.', ',')}/order_history", self.order_history)
        
        # Fetch and update Seller's order list
        _, seller = get_user(product.seller_id)
        seller_order_history = seller.order_history
        seller_order_history["order_history"].append(order_id)
        db_manager.patch(product.seller_id, f"users/{product.seller_id.replace('.', ',')}/order_history", seller_order_history)
        
        return (True, f"Order {order_id} placed successfully")

    def checkout(self):
        db_manager = DBManager()
        if not self.cart:
            return (False, "Your cart is empty")
        
        for item_id in self.cart["cart"][1:]:  # Iterate over a copy of the cart, skip dummy
            if item_id is not None:
                self.make_order(item_id)
        
        self.cart["cart"] = ["dummy"]  # Clear the cart after checkout
        db_manager.patch(self.email, f"users/{self.email.replace('.', ',')}/cart", self.cart)
        return (True, "Checkout successful, all orders placed")
    
    
class Seller(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def create_product_for_sell(self, item_name, price, description, category, pictures, inventory):
        item_id = str(uuid.uuid4())  # Generate a unique product ID
        product_data = {
            "item_id": item_id,
            "item_name": item_name,
            "price": price,
            "description": description,
            "category": category,
            "pictures": pictures,
            "seller_id": self.email,
            "inventory": inventory
        }
        
        db_manager = DBManager()
        db_manager.insert_product(product_data)
        
        self.product_listings["product_listings"].append(item_id)

        db_manager.patch(self.email, f"users/{self.email.replace('.', ',')}/product_listings", self.product_listings)
        return (True, f"Product {item_id} created for sale")

    def delete_product(self, item_id):
        db_manager = DBManager()
        db_manager.delete_product(item_id)
        if item_id in self.product_listings["product_listings"]:
            self.product_listings["product_listings"].remove(item_id)
            db_manager.patch(self.email, f"users/{self.email.replace('.', ',')}/product_listings", self.product_listings)
        return (True, "Product deleted successfully")
    
    def update_inventory(self, item_id, new_inventory):
        db_manager = DBManager()
        db_manager.update_product_inventory(item_id, new_inventory)
        return (True, "Inventory updated successfully")

    def get_my_products(self):
        if self.product_listings is None:
            self.product_listings = {'product_listings': []}
        item_ids = self.product_listings["product_listings"]
        products = []
        for item_id in item_ids:
            if item_id != "dummy":
                success, product = get_product(item_id)
                if success:
                    products.append(product)
        return (True, products)
    
    def get_order_history(self):
        db_manager = DBManager()
        order_ids = self.order_history["order_history"]
        orders = []
        for order_id in order_ids:
            if order_id != "dummy":
                success, order = get_order(order_id)
                if success:
                    orders.append(order)
        return (True, orders)
    
class Admin(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_manager = DBManager()
    
    def insert_user(self, user_data):
        self.db_manager.insert_user(user_data)

    def modify_user(self, email, user_data):
        self.db_manager.modify_user(email, user_data)

    def delete_user(self, email):
        # also deletes products under the user if the user is a seller
        duser = self.get_user(email)
        if duser['user_role'] == 'seller':
            duser_object = Seller(**duser)
            for item_id in duser_object.product_listings["product_listings"]:
                self.db_manager.delete_product(item_id)
        self.db_manager.delete_user(email)

    def get_user(self, email):
        return self.db_manager.get_user(email)

    def insert_product(self, product_data):
        seller_exists, seller = get_user(product_data["seller_id"])
        item_id = str(uuid.uuid4()) 
        product_data['item_id']=item_id
        if seller_exists:
            seller.product_listings["product_listings"].append(product_data["item_id"])
            self.db_manager.patch(seller.email, f"users/{seller.email.replace('.', ',')}/product_listings", seller.product_listings)
        self.db_manager.insert_product(product_data)

    def modify_product(self, item_id, product_data):
        self.db_manager.modify_product(item_id, product_data)

    def delete_product(self, item_id):
        # seller's products delete the new product
        success, product = get_product(item_id)
        if success:
            duser = self.get_user(product.seller_id)
            if duser:
                duser_object = Seller(**duser)
                
                if item_id in duser_object.product_listings["product_listings"]:
                    duser_object.product_listings["product_listings"].remove(item_id)
                    self.db_manager.patch(duser_object.email, f"users/{duser_object.email.replace('.', ',')}/product_listings", duser_object.product_listings)
                
            self.db_manager.delete_product(item_id)

    def get_product(self, item_id):
        return self.db_manager.get_product(item_id)

    def insert_order(self, order_data):
        # buyer's and seller's order history add the new order
        buyer_exists, buyer = get_user(order_data["buyer_id"])
        seller_exists, seller = get_user(order_data["seller_id"])
        order_id = str(uuid.uuid4()) 
        order_data['order_id']=order_id
        if buyer_exists:
            if buyer.order_history is None:
                buyer.order_history = {'order_history': []}
            buyer.order_history["order_history"].append(order_data["order_id"])
            self.db_manager.patch(buyer.email, f"users/{buyer.email.replace('.', ',')}/order_history", buyer.order_history)
        
        if seller_exists:
            seller.order_history["order_history"].append(order_data["order_id"])
            self.db_manager.patch(seller.email, f"users/{seller.email.replace('.', ',')}/order_history", seller.order_history)
        
        self.db_manager.insert_order(order_data)


    def modify_order(self, order_id, order_data):
        self.db_manager.modify_order(order_id, order_data)

    def delete_order(self, order_id):
        # buyer's and seller's order history delete the new order
        order_data = self.get_order(order_id)
        buyer_exists, buyer = get_user(order_data["buyer_id"])
        seller_exists, seller = get_user(order_data["seller_id"])
        if buyer_exists:
            if buyer.order_history is None:
                buyer.order_history = {'order_history': []}
            else:
                if order_data['order_id'] in buyer.order_history['order_history']:
                    buyer.order_history["order_history"].remove(order_data["order_id"])
                    self.db_manager.patch(buyer.email, f"users/{buyer.email.replace('.', ',')}/order_history", buyer.order_history)
                else:
                    print("The order is not in the buyer's order history.")
                
        if seller_exists:
            if order_data['order_id'] in seller.order_history['order_history']:
                seller.order_history["order_history"].remove(order_data["order_id"])
                self.db_manager.patch(seller.email, f"users/{seller.email.replace('.', ',')}/order_history", seller.order_history)
            else:
                print("The order is not in the seller's order history.")
        self.db_manager.delete_order(order_id)


    def get_order(self, order_id):
        return self.db_manager.get_order(order_id)
    
    def get_all_users(self):
        return self.db_manager.get_all_users()
    
    def get_all_products(self):
        return self.db_manager.get_all_products()
    
    def get_all_orders(self):
        return self.db_manager.get_all_orders()


def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    return stored_password == hash_password(provided_password)

def signup(email, user_name, first_name, last_name, password, user_role):
    global current_user

    hashed_password = hash_password(password)
    user_data = {
        "email": email,
        "user_name": user_name,
        "first_name": first_name,
        "last_name": last_name,
        "sha_hashed_password": hashed_password,
        "user_role": user_role,
        "order_history": {"order_history": ["dummy"]},
    }
    db_manager = DBManager()
    user_existed = db_manager.get_user(email)
    #print(email, user_existed, user_data)
    if user_existed:
        return (False, "Already signed up")
    db_manager.insert_user(user_data)
    
    # Initialize the current user based on the role
    if user_role == "buyer":
        current_user = Buyer(**user_data)
        db_manager.put(current_user.email, f"users/{current_user.email.replace('.', ',')}/cart", {"cart": ["dummy"]})
        db_manager.put(current_user.email, f"users/{current_user.email.replace('.', ',')}/order_history", {"order_history": ["dummy"]})
    elif user_role == "seller":
        current_user = Seller(**user_data)
        db_manager.put(current_user.email, f"users/{current_user.email.replace('.', ',')}/product_listings", {"product_listings": ["dummy"]})
    elif user_role == "admin":
        current_user = Admin(**user_data)
    else:
        raise (False, "Invalid user role")
    
    return (True, "Signup successful")

def signin(email, password):
    global current_user
    db_manager = DBManager()
    user_data = db_manager.get_user(email)    
    if not user_data:
        return (False, "Invalid email or password")
    #print(user_data)
    if user_data and verify_password(user_data["sha_hashed_password"], password):
        user_role = user_data.get("user_role")
        #print(user_role)
        if user_role == "buyer":
            current_user = Buyer(**user_data)
        elif user_role == "seller":
            current_user = Seller(**user_data)
        elif user_role == "admin":
            current_user = Admin(**user_data)
        else:
            raise ValueError("Invalid user role "+user_role)
        return (True, "Signin successful")
    else:
        return (False, "Invalid email or password")

def logout():
    global current_user
    current_user = None

def get_product_list_details(item_ids):
    return (True, [get_product(item_id) for item_id in item_ids])

def get_order_list_details(order_ids):
    return (True, [get_order(order_id) for order_id in order_ids])

def get_user(user_id):
    # user_id: email
    db_manager = DBManager()
    user_data = db_manager.get(user_id, f"users/{user_id.replace('.', ',')}")
    if user_data:
        return (True, User(**user_data))
    else:
        return (False, "user not found")
