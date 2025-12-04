#!/usr/bin/env python3

from faker import Faker
import random
from ..models import engine, Base
from ..models.user import User
from ..models.dealership import Dealership
from ..models.car import Car
from ..models.sale import Sale

fake = Faker()

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

def seed_users():
    """Create sample users including admins and customers"""
    users_data = [
        ("admin1", "admin1@mbuu.com", "password123", True),
        ("admin2", "admin2@mbuu.com", "password123", True),
        ("john_doe", "john@email.com", "password123", False),
        ("jane_smith", "jane@email.com", "password123", False),
        ("mike_wilson", "mike@email.com", "password123", False),
    ]
    
    users = []
    for username, email, password, is_admin in users_data:
        user = User.create(username, email, password, is_admin)
        users.append(user)
        print(f"✅ Created {'admin' if is_admin else 'user'}: {username}")
    
    return users

def seed_dealerships(users):
    """Create sample dealerships"""
    admin_users = [u for u in users if u.is_admin]
    
    dealerships_data = [
        ("Premium Motors", "123 Main St, New York, NY"),
        ("Elite Auto Sales", "456 Oak Ave, Los Angeles, CA"),
        ("Luxury Car Hub", "789 Pine Rd, Chicago, IL"),
        ("Metro Auto Center", "321 Elm St, Houston, TX"),
    ]
    
    dealerships = []
    for name, location in dealerships_data:
        admin = random.choice(admin_users)
        dealership = Dealership.create(name, location, admin.id)
        dealerships.append(dealership)
        print(f"✅ Created dealership: {name} (Admin: {admin.username})")
    
    return dealerships