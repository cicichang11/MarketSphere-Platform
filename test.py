import sys
from pathlib import Path
import unittest

# Add the parent directory to sys.path to make the backend package available
sys.path.append(str(Path(__file__).resolve().parent))

from backend.user import * 
from backend.order import * 
from backend.product import * 

class TestUserManagement(unittest.TestCase):
    
    def test_user_signup_signin_logout(self):
        # Test initial state (should be None)
        logout()
        self.assertIsNone(get_current_user())
        
        # Test seller sign up
        seller_email = "sell@example.com"
        seller_password = "password123"
        signup_result = signup(seller_email, "sellerUser", "Seller", "Example", seller_password, "seller")
        self.assertTrue(signup_result[0])
        
        # Test current user after seller sign up (should not be None)
        self.assertIsNotNone(get_current_user())
        self.assertEqual(get_current_user().email, seller_email)
        
        # Test logout after seller sign up
        logout()
        self.assertIsNone(get_current_user())
        
        # Test seller sign in
        signin_result = signin(seller_email, seller_password)
        self.assertTrue(signin_result[0])
        self.assertEqual(get_current_user().email, seller_email)
        
        # Test logout after seller sign in
        logout()
        self.assertIsNone(get_current_user())
        
        # Test buyer sign up
        buyer_email = "buyer@example.com"
        buyer_password = "password456"
        signup(buyer_email, "buyerUser", "Buyer", "Example", buyer_password, "buyer")
        logout()  # Ensure a clean state
        
        # Test current user after buyer sign up (should be None due to logout)
        self.assertIsNone(get_current_user())
        
        # Test buyer sign in
        signin(buyer_email, buyer_password)
        
        # Test current user after buyer sign in
        self.assertIsNotNone(get_current_user())
        self.assertEqual(get_current_user().email, buyer_email)
        logout()

    def test_seller_creates_products(self):
        seller_email = "sell@example.com"
        seller_password = "password123"
        signin(seller_email, seller_password)
        current_user = get_current_user()
        self.assertEqual(current_user.email, seller_email)
        print("Signed in as a " + current_user.user_role)
        
        
        current_user.create_product_for_sell("Product 1", 100, "Description of Product 1", "Electronics", ["pic1.jpg"], 10)
        current_user.create_product_for_sell("Product 2", 200, "Description of Product 2", "Books", ["pic2.jpg"], 5)
        
        # Verify the seller now has 2 products listed
        print(current_user.get_my_products())
        print(search_products("Product"))
        logout()
        
    def test_buyer_search_add_checkout(self):
        seller_email = "buyer@example.com"
        seller_password = "password456"
        signin(seller_email, seller_password)

        search_results = search_products("Product")
        category_results = browse_products_by_category("Electronics")


if __name__ == '__main__':
    unittest.main()

