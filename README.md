# Distributed Database - MarketSphere-Platform
Demo Video: https://youtu.be/W2vhFi16tzI

## Overview
MarketSphere is a distributed e-commerce platform that allows users to buy and sell products. It utilizes a distributed database system to ensure scalability and fault tolerance.


## Project Structure
The project is structured into the following modules:

- `app.py`: The main Flask application file that defines the routes and handles user interactions.
- `distributed_db.py`: Defines the DistributedDB class, which manages the interaction with the distributed databases.
- `db_manager.py`: Contains the DBManager class, which extends DistributedDB and provides higher-level methods for managing users, products, and orders.
- `user.py`: Defines the User class and its subclasses (Buyer, Seller, and Admin), and handles user-related operations like signup and signin.
- `product.py`: Defines the Product class and provides functions for creating, retrieving, browsing, and searching products.
- `order.py`: Defines the Order class and handles order creation and retrieval.
- `admin_panel.py`: Streamlit application for the admin panel.

## Distributed Database System
MarketSphere utilizes a distributed database system to handle user data, product listings, and order management. The system is designed to ensure scalability and fault tolerance by distributing data across multiple databases using a hash function.

- The DistributedDB class in distributed_db.py manages the interaction with the distributed databases.
- The system uses two Firebase database URLs defined in the db_urls list.
- The compute_hash method in DistributedDB is responsible for evenly distributing data across the databases based on a hash value computed from the item's unique identifier.


## User Roles and Functionality
MarketSphere supports three user roles: Buyer, Seller, and Admin.

### Buyer

- Buyers can browse and search for products by category or search term.
- They can add products to their cart, remove items from the cart, and proceed to checkout.
- Buyers have access to their order history.

### Seller

- Sellers can create new product listings by providing details such as name, price, description, category, pictures, and inventory.
- They can update the inventory of their listed products.
- Sellers have access to their product listings and order history.

### Admin

- Admins have access to an admin panel where they can manage users, products, and orders.
- They can delete users, products, and orders.
- Admins can modify user information, product details, and order status.
- They can also insert new users, products, and orders into the system.


## Technologies Used
- **Frontend:** HTML, TailwindCSS, JavaScript
- **Backend:** Python Flask (assumed based on the form handling and route management)
- **Database:** Firebase as a backend service which includes features for real-time data synchronization across user devices


## Installation and Usage
Install Streamlit: `pip install streamlit`

Run the application: `streamlit run app.py`

