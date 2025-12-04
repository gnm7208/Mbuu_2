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

def seed_cars(dealerships):
    """Create sample car inventory"""
    car_brands = ["Toyota", "Honda", "BMW", "Mercedes", "Audi", "Ford", "Chevrolet", "Nissan"]
    car_models = {
        "Toyota": ["Camry", "Corolla", "RAV4", "Prius"],
        "Honda": ["Civic", "Accord", "CR-V", "Pilot"],
        "BMW": ["3 Series", "5 Series", "X3", "X5"],
        "Mercedes": ["C-Class", "E-Class", "GLC", "GLE"],
        "Audi": ["A4", "A6", "Q5", "Q7"],
        "Ford": ["F-150", "Mustang", "Explorer", "Escape"],
        "Chevrolet": ["Silverado", "Equinox", "Malibu", "Tahoe"],
        "Nissan": ["Altima", "Sentra", "Rogue", "Pathfinder"]
    }
    colors = ["Black", "White", "Silver", "Red", "Blue", "Gray"]
    
    cars = []
    for dealership in dealerships:
        num_cars = random.randint(8, 12)
        for _ in range(num_cars):
            brand = random.choice(car_brands)
            model = random.choice(car_models[brand])
            year = random.randint(2018, 2024)
            price = random.randint(15000, 80000)
            color = random.choice(colors)
            
            car = Car.create(brand, model, year, price, color, dealership.id)
            cars.append(car)
        
        print(f"✅ Created {num_cars} cars for {dealership.name}")
    
    return cars

def seed_sales(users, cars):
    """Create sample sales transactions"""
    customer_users = [u for u in users if not u.is_admin]
    available_cars = [c for c in cars if not c.is_sold]
    
    num_sales = min(15, len(available_cars))
    sales = []
    
    for _ in range(num_sales):
        customer = random.choice(customer_users)
        car = random.choice(available_cars)
        available_cars.remove(car)
        
        sale_price = car.price * random.uniform(0.95, 1.05)
        
        sale = Sale.create(customer.id, car.id, car.dealership_id, sale_price)
        car.mark_sold()
        sales.append(sale)
        
        print(f"✅ Created sale: {customer.username} bought {car.brand} {car.model}")
    
    return sales