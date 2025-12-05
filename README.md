# Mbuu - Car Dealership Management CLI

Mbuu is a command-line interface application for managing car dealerships where admins can sell cars of different brands from their registered dealerships to authenticated users.

## Project Overview

This CLI application solves the real-world problem of managing car dealership operations, including:
- User authentication and registration
- Dealership management for admins
- Car inventory management with multiple brands
- Sales transaction processing between customers and dealerships

## Learning Goals & Technical Concepts

This Phase 3 project demonstrates proficiency in the following areas:

### 1. **CLI Application Best Practices**
- Role-based menu systems (Guest, Customer, Admin)
- Error handling and input validation
- User-friendly interface with clear feedback
- Proper separation of concerns (CLI vs. business logic)

### 2. **SQLAlchemy ORM with Multiple Related Tables**
The application implements 4 interconnected tables with proper relationships:
- **Users** table: Stores user credentials and role information
- **Dealerships** table: Represents dealership entities with admin ownership (one-to-many with User)
- **Cars** table: Inventory items with dealership association (one-to-many with Dealership)
- **Sales** table: Transaction records connecting users, cars, and dealerships (many-to-many bridge with foreign keys to User, Car, and Dealership)

#### Relationship Map:
- User ↔ Dealership (one-to-many): Admin manages multiple dealerships
- User ↔ Sale (one-to-many): Customer makes multiple purchases
- Dealership ↔ Car (one-to-many): Dealership has multiple cars in inventory
- Dealership ↔ Sale (one-to-many): Dealership processes multiple sales
- Car ↔ Sale (one-to-one): Each car results in at most one sale
- Sale connects: Customer + Car + Dealership (many-to-many relationships)

### 3. **Virtual Environment Management with Pipenv**
- `Pipfile` specifies all project dependencies
- Reproducible environment across different machines
- Separate dev and production dependencies

### 4. **Professional Package Structure**
```
lib/
├── __init__.py              # Package initialization
├── cli.py                   # CLI interface and menu handling
├── helpers.py               # Business logic and helper functions
├── debug.py                 # Debug utilities
├── models/
│   ├── __init__.py          # Database configuration (engine, sessionmaker)
│   ├── user.py              # User ORM model
│   ├── dealership.py        # Dealership ORM model
│   ├── car.py               # Car ORM model
│   └── sale.py              # Sale ORM model
└── db/
    ├── __init__.py          # Database package initialization
    ├── models.py            # ORM base configuration
    └── seed.py              # Database seeding with sample data
```

### 5. **Data Structures Usage**
- **Lists**: Used throughout for storing collections (users, dealerships, cars, sales)
  - Menu options, search results, user/car listings
  - Dynamic list filtering for available cars, admin-owned dealerships
- **Dictionaries**: Menu choice mapping for efficient command routing
  - `guest_choices`, `admin_choices`, `customer_choices` dictionaries map user input to functions
- **Tuples**: Used for immutable data grouping
  - Seed data structured as tuples for user credentials and dealership info
  - Function return patterns where appropriate

## Features

- **User Management**: Registration, login, and role-based access (Admin/Customer)
- **Dealership Operations**: Create and manage multiple dealerships
- **Car Inventory**: Add, view, search, and manage car inventory
- **Sales Processing**: Complete car purchase transactions
- **Reporting**: View sales history and statistics

## Installation

1. Clone the repository or navigate to project directory
2. Install Pipenv (if not already installed): `pip install pipenv`
3. Install dependencies: `pipenv install`
4. Activate virtual environment: `pipenv shell`
5. Initialize database: `python lib/db/seed.py`
6. Run the application: `python run.py`

**Alternatively**, run directly without shell activation:
- Initialize DB: `pipenv run python lib/db/seed.py`
- Run app: `pipenv run python run.py`

## Database Schema

The application uses SQLAlchemy ORM with the following models:
- **User**: Manages customer accounts and authentication (one-to-many with Dealership and Sale)
- **Dealership**: Represents car dealerships managed by admins (one-to-many with Car and Sale)
- **Car**: Individual car inventory items (one-to-one with Sale)
- **Sale**: Transaction records between users and dealerships

## Usage

The application provides different interfaces based on user role:
- **Guests**: Can browse cars, search by brand, and register/login
- **Customers**: Can purchase cars and view purchase history
- **Admins**: Can manage dealerships, add cars to inventory, and view sales reports

## Sample Login Credentials

After running the seed script, you can use these accounts:
- **Admin**: username: `admin1`, password: `password123`
- **Customer**: username: `john_doe`, password: `password123`

## Project Structure

- `run.py`: Entry point for the application
- `lib/cli.py`: Main CLI interface with role-based menus
- `lib/helpers.py`: Helper functions for all operations
- `lib/models/`: Database models (User, Dealership, Car, Sale)
- `lib/db/seed.py`: Database seeding with sample data
- `lib/debug.py`: Debug utilities for testing

## Technical Implementation Details

### Error Handling
- Input validation for all user inputs
- Exception handling for database operations
- Graceful error messages for invalid operations
- Try-except blocks in CRUD operations to catch and report errors

### Code Quality & Best Practices
- Clear function documentation with docstrings
- Consistent naming conventions (snake_case for functions/variables)
- DRY principle: Reusable helper functions
- Proper separation of concerns (models, helpers, CLI)
- Type-appropriate data structures (lists for collections, dicts for mappings, tuples for immutable groupings)

### Database Design
- Proper use of foreign keys for referential integrity
- Cascading deletes for data consistency (dealership deletion removes associated cars)
- One-to-one and one-to-many relationships properly modeled
- Class methods for common queries (find_by_id, find_by_brand, etc.)

## Deployment Notes

- Database file (`mbuu.db`) is created automatically in the project root
- Application uses SQLite for portability
- All dependencies specified in `Pipfile` for reproducible environments
- Run with Python 3.8+