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