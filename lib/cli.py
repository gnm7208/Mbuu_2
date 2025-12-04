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

if __name__ == "__main__":
    main()