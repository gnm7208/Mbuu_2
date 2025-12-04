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

# User Management Functions
def list_all_users():
    """Display all users"""
    users = User.get_all()
    if not users:
        print("📭 No users found.")
        return
    
    print("\n=== ALL USERS ===")
    for user in users:
        print(f"ID: {user.id} | {user.full_info}")

def delete_user():
    """Delete a user by ID"""
    if not current_user or not current_user.is_admin:
        print("❌ Admin access required!")
        return
    
    list_all_users()
    try:
        user_id = int(input("\nEnter user ID to delete: "))
        user = User.find_by_id(user_id)
        if user:
            user.delete()
            print(f"✅ User {user.username} deleted successfully!")
        else:
            print("❌ User not found!")
    except ValueError:
        print("❌ Invalid user ID!")

# Dealership Management Functions
def create_dealership():
    """Create a new dealership"""
    if not current_user or not current_user.is_admin:
        print("❌ Admin access required!")
        return
    
    print("\n=== CREATE DEALERSHIP ===")
    name = input("Dealership name: ").strip()
    location = input("Location: ").strip()
    
    if not name or not location:
        print("❌ Name and location are required!")
        return
    
    try:
        dealership = Dealership.create(name, location, current_user.id)
        print(f"✅ Dealership '{name}' created successfully!")
    except Exception as e:
        print(f"❌ Failed to create dealership: {str(e)}")

def list_dealerships():
    """Display all dealerships"""
    dealerships = Dealership.get_all()
    if not dealerships:
        print("📭 No dealerships found.")
        return
    
    print("\n=== ALL DEALERSHIPS ===")
    for dealership in dealerships:
        print(f"ID: {dealership.id} | {dealership.name} - {dealership.location}")
        print(f"   Admin: {dealership.admin.username} | Cars: {dealership.car_count} | Sales: {dealership.total_sales}")

def view_my_dealerships():
    """View dealerships owned by current admin"""
    if not current_user or not current_user.is_admin:
        print("❌ Admin access required!")
        return
    
    dealerships = Dealership.find_by_admin(current_user.id)
    if not dealerships:
        print("📭 You don't own any dealerships.")
        return
    
    print(f"\n=== {current_user.username.upper()}'S DEALERSHIPS ===")
    for dealership in dealerships:
        print(f"ID: {dealership.id} | {dealership.name} - {dealership.location}")
        print(f"   Cars: {dealership.car_count} | Sales: {dealership.total_sales}")

def delete_dealership():
    """Delete a dealership"""
    if not current_user or not current_user.is_admin:
        print("❌ Admin access required!")
        return
    
    view_my_dealerships()
    try:
        dealership_id = int(input("\nEnter dealership ID to delete: "))
        dealership = Dealership.find_by_id(dealership_id)
        
        if not dealership:
            print("❌ Dealership not found!")
            return
        
        if dealership.admin_id != current_user.id:
            print("❌ You can only delete your own dealerships!")
            return
        
        dealership.delete()
        print(f"✅ Dealership '{dealership.name}' deleted successfully!")
    except ValueError:
        print("❌ Invalid dealership ID!")

# Car Management Functions
def list_all_cars():
    """Display all cars"""
    cars = Car.get_all()
    if not cars:
        print("📭 No cars found.")
        return
    
    print("\n=== ALL CARS ===")
    for car in cars:
        print(f"ID: {car.id} | {car.full_description}")
        print(f"   Dealership: {car.dealership.name}")

def list_available_cars():
    """Display available cars for purchase"""
    cars = Car.get_available()
    if not cars:
        print("📭 No cars available for purchase.")
        return
    
    print("\n=== AVAILABLE CARS ===")
    for car in cars:
        print(f"ID: {car.id} | {car.full_description}")
        print(f"   Dealership: {car.dealership.name} - {car.dealership.location}")

def search_cars_by_brand():
    """Search cars by brand"""
    brand = input("Enter brand to search: ").strip()
    cars = Car.find_by_brand(brand)
    
    if not cars:
        print(f"📭 No cars found for brand: {brand}")
        return
    
    print(f"\n=== CARS MATCHING '{brand.upper()}' ===")
    for car in cars:
        print(f"ID: {car.id} | {car.full_description}")
        print(f"   Dealership: {car.dealership.name}")