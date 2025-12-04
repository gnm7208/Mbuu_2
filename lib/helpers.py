from models.user import User
from models.dealership import Dealership
from models.car import Car
from models.sale import Sale

# Global variable to track current logged-in user
current_user = None

def exit_program():
    """Exit the application"""
    print("🚗 Thank you for using Mbuu! Drive safely! 🚗")
    exit()

def authenticate_user():
    """Handle user login"""
    global current_user
    print("\n=== LOGIN ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    user = User.find_by_username(username)
    if user and user.password == password:
        current_user = user
        print(f"✅ Welcome back, {user.username}!")
        return True
    else:
        print("❌ Invalid credentials!")
        return False

def register_user():
    """Handle user registration"""
    print("\n=== REGISTER ===")
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    if User.find_by_username(username):
        print("❌ Username already exists!")
        return False
    
    try:
        user = User.create(username, email, password, False)
        print(f"✅ Account created successfully! Welcome, {username}!")
        return True
    except Exception as e:
        print(f"❌ Registration failed: {str(e)}")
        return False

def logout_user():
    """Handle user logout"""
    global current_user
    if current_user:
        print(f"👋 Goodbye, {current_user.username}!")
        current_user = None
    else:
        print("❌ No user is currently logged in!")