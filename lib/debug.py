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

if __name__ == "__main__":
    print("🚗 Mbuu Debug Console 🚗")
    test_models()