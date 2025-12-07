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

def demo_relationships():
    """Demo SQLAlchemy relationship automatic fetching"""
    from models import get_session
    
    print("\n" + "="*60)
    print("🔗 DEMONSTRATING SQLALCHEMY RELATIONSHIPS")
    print("="*60)
    
    session = get_session()
    try:
        sales = session.query(Sale).all()
        
        if not sales:
            print("❌ No sales found. Run seed.py first.")
            return
        
        sale = sales[0]
        
        print(f"\n📊 Sale ID: {sale.id}")
        print(f"💰 Sale Price: ${sale.sale_price:,.2f}")
        
        print("\n--- Accessing Related Data Through Relationships ---")
        
        # Customer relationship
        print(f"\n👤 Customer (via sale.customer):")
        print(f"   Username: {sale.customer.username}")
        print(f"   Email: {sale.customer.email}")
        print(f"   Role: {'Admin' if sale.customer.is_admin else 'Customer'}")
        
        # Car relationship
        print(f"\n🚗 Car (via sale.car):")
        print(f"   Brand: {sale.car.brand}")
        print(f"   Model: {sale.car.model}")
        print(f"   Year: {sale.car.year}")
        print(f"   Color: {sale.car.color}")
        
        # Dealership relationship
        print(f"\n🏢 Dealership (via sale.dealership):")
        print(f"   Name: {sale.dealership.name}")
        print(f"   Location: {sale.dealership.location}")
        
        print("\n✅ All data fetched automatically through SQLAlchemy relationships!")
        print("   No manual SQL joins required.\n")
    finally:
        session.close()

if __name__ == "__main__":
    print("🚗 Mbuu Debug Console 🚗")
    test_models()
    demo_relationships()