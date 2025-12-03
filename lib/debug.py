#!/usr/bin/env python3

"""
Debug script for testing Mbuu application functionality
"""

from models.user import User
from models.dealership import Dealership
from models.car import Car
from models.sale import Sale

def test_models():
    """Test all model operations"""
    print("🧪 Testing Mbuu Models...")
    
    # Test User model
    print("\n--- Testing User Model ---")
    users = User.get_all()
    print(f"Total users: {len(users)}")
    
    if users:
        user = users[0]
        print(f"First user: {user.full_info}")
    
    # Test Dealership model
    print("\n--- Testing Dealership Model ---")
    dealerships = Dealership.get_all()
    print(f"Total dealerships: {len(dealerships)}")
    
    if dealerships:
        dealership = dealerships[0]
        print(f"First dealership: {dealership.name} - {dealership.location}")
        print(f"Cars in dealership: {dealership.car_count}")
    
    # Test Car model
    print("\n--- Testing Car Model ---")
    cars = Car.get_all()
    available_cars = Car.get_available()
    print(f"Total cars: {len(cars)}")
    print(f"Available cars: {len(available_cars)}")
    
    if cars:
        car = cars[0]
        print(f"First car: {car.full_description}")
    
    # Test Sale model
    print("\n--- Testing Sale Model ---")
    sales = Sale.get_all()
    print(f"Total sales: {len(sales)}")
    
    if sales:
        sale = sales[0]
        print(f"First sale: {sale.sale_summary}")

def test_relationships():
    """Test model relationships"""
    print("\n🔗 Testing Model Relationships...")
    
    # Test User -> Dealership relationship
    admins = [u for u in User.get_all() if u.is_admin]
    if admins:
        admin = admins[0]
        print(f"\nAdmin {admin.username} owns {len(admin.dealerships)} dealerships:")
        for dealership in admin.dealerships:
            print(f"  - {dealership.name}")
    
    # Test Dealership -> Car relationship
    dealerships = Dealership.get_all()
    if dealerships:
        dealership = dealerships[0]
        print(f"\n{dealership.name} has {len(dealership.cars)} cars:")
        for car in dealership.cars[:3]:  # Show first 3 cars
            print(f"  - {car.full_description}")
    
    # Test Customer purchases
    customers = [u for u in User.get_all() if not u.is_admin]
    if customers:
        customer = customers[0]
        print(f"\nCustomer {customer.username} has {len(customer.purchases)} purchases:")
        for purchase in customer.purchases:
            print(f"  - {purchase.sale_summary}")

def interactive_debug():
    """Interactive debugging session"""
    print("\n🔧 Interactive Debug Mode")
    print("Available commands:")
    print("  users - List all users")
    print("  dealerships - List all dealerships")
    print("  cars - List all cars")
    print("  sales - List all sales")
    print("  test - Run model tests")
    print("  relationships - Test relationships")
    print("  quit - Exit debug mode")
    
    while True:
        try:
            command = input("\ndebug> ").strip().lower()
            
            if command == "quit":
                break
            elif command == "users":
                users = User.get_all()
                for user in users:
                    print(f"  {user.id}: {user.full_info}")
            elif command == "dealerships":
                dealerships = Dealership.get_all()
                for dealership in dealerships:
                    print(f"  {dealership.id}: {dealership.name} - {dealership.location}")
            elif command == "cars":
                cars = Car.get_all()
                for car in cars[:10]:  # Limit to first 10
                    print(f"  {car.id}: {car.full_description}")
            elif command == "sales":
                sales = Sale.get_all()
                for sale in sales:
                    print(f"  {sale.id}: {sale.sale_summary}")
            elif command == "test":
                test_models()
            elif command == "relationships":
                test_relationships()
            else:
                print("❌ Unknown command")
        
        except KeyboardInterrupt:
            print("\n👋 Exiting debug mode...")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚗 Mbuu Debug Console 🚗")
    test_models()
    test_relationships()
    interactive_debug()