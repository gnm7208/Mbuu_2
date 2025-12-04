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

def purchase_car():
    """Allow customer to purchase a car"""
    if not current_user:
        print("❌ Please login first!")
        return
    
    if current_user.is_admin:
        print("❌ Admins cannot purchase cars!")
        return
    
    list_available_cars()
    
    try:
        car_id = int(input("\nEnter car ID to purchase: "))
        car = Car.find_by_id(car_id)
        
        if not car:
            print("❌ Car not found!")
            return
        
        if car.is_sold:
            print("❌ Car is already sold!")
            return
        
        print(f"\n🚗 Car Details: {car.full_description}")
        print(f"📍 Dealership: {car.dealership.name} - {car.dealership.location}")
        
        confirm = input(f"\nConfirm purchase for ${car.price:,.2f}? (y/n): ").lower()
        if confirm != 'y':
            print("❌ Purchase cancelled.")
            return
        
        sale = Sale.create(current_user.id, car.id, car.dealership_id, car.price)
        car.mark_sold()
        
        print(f"🎉 Congratulations! You purchased the {car.year} {car.brand} {car.model}!")
        print(f"💰 Total paid: ${sale.sale_price:,.2f}")
        
    except ValueError:
        print("❌ Invalid car ID!")

def view_my_purchases():
    """View customer's purchase history"""
    if not current_user:
        print("❌ Please login first!")
        return
    
    sales = Sale.find_by_customer(current_user.id)
    if not sales:
        print("📭 You haven't made any purchases yet.")
        return
    
    print(f"\n=== {current_user.username.upper()}'S PURCHASES ===")
    total_spent = 0
    for sale in sales:
        print(f"🚗 {sale.car.year} {sale.car.brand} {sale.car.model}")
        print(f"   Price: ${sale.sale_price:,.2f} | Date: {sale.sale_date.strftime('%Y-%m-%d')}")
        print(f"   From: {sale.dealership.name}")
        total_spent += sale.sale_price
    
    print(f"\n💰 Total spent: ${total_spent:,.2f}")

def display_stats():
    """Display system statistics"""
    users = User.get_all()
    dealerships = Dealership.get_all()
    cars = Car.get_all()
    sales = Sale.get_all()
    
    print("\n=== MBUU STATISTICS ===")
    print(f"👥 Total Users: {len(users)}")
    print(f"   - Admins: {len([u for u in users if u.is_admin])}")
    print(f"   - Customers: {len([u for u in users if not u.is_admin])}")
    print(f"🏢 Total Dealerships: {len(dealerships)}")
    print(f"🚗 Total Cars: {len(cars)}")
    print(f"   - Available: {len([c for c in cars if not c.is_sold])}")
    print(f"   - Sold: {len([c for c in cars if c.is_sold])}")
    print(f"💰 Total Sales: {len(sales)}")
    
    if sales:
        total_revenue = sum(sale.sale_price for sale in sales)
        print(f"💵 Total Revenue: ${total_revenue:,.2f}")

def add_car():
    """Add a new car to dealership inventory"""
    if not current_user or not current_user.is_admin:
        print("❌ Admin access required!")
        return
    
    dealerships = Dealership.find_by_admin(current_user.id)
    if not dealerships:
        print("❌ You must own a dealership to add cars!")
        return
    
    print("\n=== ADD CAR ===")
    print("Your dealerships:")
    for i, dealership in enumerate(dealerships, 1):
        print(f"{i}. {dealership.name}")
    
    try:
        choice = int(input("Select dealership (number): ")) - 1
        if choice < 0 or choice >= len(dealerships):
            print("❌ Invalid selection!")
            return
        
        dealership = dealerships[choice]
        
        brand = input("Car brand: ").strip()
        model = input("Car model: ").strip()
        year = int(input("Year: "))
        price = float(input("Price: $"))
        color = input("Color: ").strip()
        
        if not all([brand, model, color]) or year < 1900 or price <= 0:
            print("❌ Invalid car details!")
            return
        
        car = Car.create(brand, model, year, price, color, dealership.id)
        print(f"✅ {year} {brand} {model} added to {dealership.name}!")
        
    except (ValueError, IndexError):
        print("❌ Invalid input!")