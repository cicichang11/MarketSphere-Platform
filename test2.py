import sys
from pathlib import Path
import unittest
from backend.db_manager import DBManager

# Add the parent directory to sys.path to make the backend package available
sys.path.append(str(Path(__file__).resolve().parent))

from backend.user import * 
from backend.order import * 
from backend.product import * 

seller_email = "sell@example.com"
seller_password = "password123"
signup_result = signup(seller_email, "sellerUser", "Seller", "Example", seller_password, "seller")
print(signup_result)
logout()



seller_email = "sell1@example.com"
seller_password = "password1234"
signup_result = signup(seller_email, "sellerUser", "Seller", "Example", seller_password, "seller")
print(signup_result)
logout()


signin(seller_email, seller_password)
current_user = get_current_user()
print("Signed in as " + current_user.email)
print(current_user.product_listings)

print(current_user.create_product_for_sell("Product 1", 100, "Description of Product 1", "Electronics", ["pic1.jpg"], 10))
print(current_user.create_product_for_sell("Product 2", 200, "Description of Product 2", "Books", ["pic2.jpg"], 5))

print(current_user.product_listings)

logout()


# buyer examples:

buyer_email = "buyer@example.com"
buyer_password = "password456"
signup(buyer_email, "buyerUser", "Buyer", "Example", buyer_password, "buyer")
signin(buyer_email, buyer_password)
current_user = get_current_user()
print("Signed in as " + current_user.email)

# buyer_email = "buyer11@example.com"
# buyer_password = "password789"


print("Search", search_products("Product"))
print("Filter by Category", browse_products_by_category("Electronics"))

successful, products = search_products("Product")
current_user.add_to_cart(products[0].item_id)
current_user.add_to_cart(products[1].item_id)
print("Cart", current_user.cart)

print("checking out")
current_user.checkout()

print("Cart", current_user.cart)
print(current_user.order_history)