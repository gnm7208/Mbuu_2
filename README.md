# Mbuu - Car Dealership Management CLI

Mbuu is a command-line interface application for managing car dealerships where admins can sell cars of different brands from their registered dealerships to authenticated users.

## Project Overview

This CLI application solves the real-world problem of managing car dealership operations, including:
- User authentication and registration
- Dealership management for admins
- Car inventory management with multiple brands
- Sales transaction processing between customers and dealerships

## Features

- **User Management**: Registration, login, and role-based access (Admin/Customer)
- **Dealership Operations**: Create and manage multiple dealerships
- **Car Inventory**: Add, view, search, and manage car inventory
- **Sales Processing**: Complete car purchase transactions
- **Reporting**: View sales history and statistics

## Installation

1. Clone the repository
2. Install dependencies: `pipenv install`
3. Activate virtual environment: `pipenv shell`
4. Initialize database: `python lib/db/seed.py`
5. Run the application: `python lib/cli.py`

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

- `lib/cli.py`: Main CLI interface with role-based menus
- `lib/helpers.py`: Helper functions for all operations
- `lib/models/`: Database models (User, Dealership, Car, Sale)
- `lib/db/seed.py`: Database seeding with sample data
- `lib/debug.py`: Debug utilities for testing