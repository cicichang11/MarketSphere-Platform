from backend.distributed_db import DistributedDB
import requests

class DBManager(DistributedDB):
    def insert_user(self, user_data):
        email = user_data.get('email')
        self.put(email, f"users/{email.replace('.', ',')}", user_data)

    def modify_user(self, email, user_data):
        self.patch(email, f"users/{email.replace('.', ',')}", user_data)

    def delete_user(self, email):
        self.delete(email, f"users/{email.replace('.', ',')}")

    def get_user(self, email):
        return self.get(email, f"users/{email.replace('.', ',')}")
    
    def insert_product(self, product_data):
        item_id = product_data.get('item_id')
        self.put(item_id, f"products/{item_id}", product_data)

    def modify_product(self, item_id, product_data):
        self.patch(item_id, f"products/{item_id}", product_data)

    def delete_product(self, item_id):
        self.delete(item_id, f"products/{item_id}")
    
    def get_product(self, item_id):
        return self.get(item_id, f"products/{item_id}")

    def insert_order(self, order_data):
        order_id = order_data.get('order_id')
        self.put(order_id, f"orders/{order_id}", order_data)

    def modify_order(self, order_id, order_data):
        self.patch(order_id, f"orders/{order_id}", order_data)

    def delete_order(self, order_id):
        self.delete(order_id, f"orders/{order_id}")

    def get_order(self, order_id):
        return self.get(order_id, f"orders/{order_id}")

    def update_product_inventory(self, item_id, new_inventory):
        inventory_data = {"inventory": new_inventory}
        self.patch(item_id, f"products/{item_id}", inventory_data)

    def search_products(self, search_term):
        results = []
        # Since data is distributed, we need to check both databases
        for db_url in self.db_urls:
            url = f"{db_url}products.json"
            response = requests.get(url)
            if response.status_code == 200:
                products = response.json()
                if products:
                    for item_id, product in products.items():
                        # Simple case-insensitive search in item_name and description
                        if search_term.lower() in product.get("item_name", "").lower() or \
                           search_term.lower() in product.get("description", "").lower():
                            results.append(product)
        return results

    def find_by_category(self, category):
        """Find products by category."""
        results = []
        # Since data is distributed, we need to check both databases
        for db_url in self.db_urls:
            url = f"{db_url}products.json"
            response = requests.get(url)
            if response.status_code == 200:
                products = response.json()
                if products:
                    for item_id, product in products.items():
                        if product.get("category", "").lower() == category.lower():
                            results.append(product)
        return results
    
    # return data (given path)from one databases
    def get_all_from_db(self, path, db_url):
        """fetch all records from one database."""
        url = f"{db_url}{path}.json"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else {}
    # return data (given path)from both databases
    def get_all_records(self, path):
        """Fetch all records from all databases for a given path."""
        all_records = {}
        for db_url in self.db_urls:
            records = self.get_all_from_db(path, db_url)
            if records:
                all_records.update(records)
        return all_records
   
    #return all users for admin
    def get_all_users(self):
        return self.get_all_records("users")
    
    #return all products for admin
    def get_all_products(self):
        return self.get_all_records("products")
    
    #return all orders for admin
    def get_all_orders(self):
        return self.get_all_records("orders")

