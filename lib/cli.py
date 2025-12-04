#!/usr/bin/env python3

from helpers import (
    exit_program, authenticate_user, register_user, logout_user,
    list_all_users, delete_user, create_dealership, list_dealerships,
    view_my_dealerships, delete_dealership, list_all_cars,
    list_available_cars, search_cars_by_brand, purchase_car,
    view_my_purchases, display_stats, current_user
)

def main():
    """Main CLI loop"""
    print("🚗 Welcome to Mbuu - Car Dealership Management System! 🚗")
    
    while True:
        if not current_user:
            guest_menu()
        elif current_user.is_admin:
            admin_menu()
        else:
            customer_menu()
        
        try:
            choice = input("\n> ").strip()
            handle_menu_choice(choice)
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {str(e)}")

def guest_menu():
    """Display menu for non-authenticated users"""
    print("\n" + "="*50)
    print("🔐 GUEST MENU")
    print("="*50)
    print("1. Login")
    print("2. Register")
    print("3. View Available Cars")
    print("4. Search Cars by Brand")
    print("5. View All Dealerships")
    print("6. System Statistics")
    print("0. Exit")

def customer_menu():
    """Display menu for authenticated customers"""
    print("\n" + "="*50)
    print(f"🛒 CUSTOMER MENU - Welcome, {current_user.username}!")
    print("="*50)
    print("1. Browse Available Cars")
    print("2. Search Cars by Brand")
    print("3. Purchase a Car")
    print("4. View My Purchases")
    print("5. View All Dealerships")
    print("6. System Statistics")
    print("7. Logout")
    print("0. Exit")

if __name__ == "__main__":
    main()