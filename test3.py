import sys
from pathlib import Path
import unittest
from backend.db_manager import DBManager

# Add the parent directory to sys.path to make the backend package available
sys.path.append(str(Path(__file__).resolve().parent))

from backend.user import * 
from backend.order import * 
from backend.product import * 



admin_email = "admin@usc.edu"
admin_password = "admin"
signup_result = signup(admin_email, "Admin", "Admin", "", admin_password, "admin")
print(signup_result)
logout()


admin_email = "admin1@usc.edu"
admin_password = "admin1"
signup_result = signup(admin_email, "Admin", "Admin", "", admin_password, "admin")
print(signup_result)
logout()