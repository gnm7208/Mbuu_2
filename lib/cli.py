#!/usr/bin/env python3

"""
CLI Interface for Mbuu - Car Dealership Management System
Provides menu-driven interface for user interaction
"""

import sys

from helpers import (
    exit_program, authenticate_user, register_user, logout_user,
    list_all_users, delete_user, create_dealership, list_dealerships,
    view_my_dealerships, delete_dealership, add_car, list_all_cars,
    list_available_cars, search_cars_by_brand, purchase_car,
    view_my_purchases, display_stats, current_user
)

# Menu choices dictionary for all roles
MENU_CHOICES = {
    "guest": {
        "1": authenticate_user,
        "2": register_user,
        "3": list_available_cars,
        "4": search_cars_by_brand,
        "5": list_dealerships,
        "6": display_stats
    },
    "admin": {
        "1": create_dealership,
        "2": view_my_dealerships,
        "3": list_dealerships,
        "4": delete_dealership,
        "5": add_car,
        "6": list_all_cars,
        "7": list_available_cars,
        "8": search_cars_by_brand,
        "9": list_all_users,
        "10": delete_user,
        "11": display_stats,
        "12": logout_user
    },
    "customer": {
        "1": list_available_cars,
        "2": search_cars_by_brand,
        "3": purchase_car,
        "4": view_my_purchases,
        "5": list_dealerships,
        "6": display_stats,
        "7": logout_user
    }
}

def main():
    """Main CLI loop"""
    print("🚗 Welcome to Mbuu - Car Dealership Management System! 🚗")
    
    while True:
        # Determine menu type
        if not current_user:
            menu_type = "guest"
        elif current_user.is_admin:
            menu_type = "admin"
        else:
            menu_type = "customer"
        
        # Display appropriate menu
        if menu_type == "guest":
            guest_menu()
        elif menu_type == "admin":
            admin_menu()
        else:
            customer_menu()
        
        try:
            choice = input("\n> ").strip()
            
            # Handle exit separately
            if choice == "0":
                exit_program()
                break
            
            handle_menu_choice(choice, menu_type)
            
            # Pause before showing menu again
            print("\n" + "="*50)
            print("DEBUG: About to show prompt")
            response = input("Press Enter to continue...")
            print(f"DEBUG: User pressed Enter, response='{response}'")
            print("\n" * 2)  # Add spacing
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {str(e)}")
            input("\n\nPress Enter to continue...")
            print("\n" * 2)

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

def admin_menu():
    """Display menu for authenticated admins"""
    print("\n" + "="*50)
    print(f"👑 ADMIN MENU - Welcome, {current_user.username}!")
    print("="*50)
    print("🏢 DEALERSHIP MANAGEMENT:")
    print("1. Create Dealership")
    print("2. View My Dealerships")
    print("3. View All Dealerships")
    print("4. Delete Dealership")
    print("\n🚗 CAR MANAGEMENT:")
    print("5. Add Car to Inventory")
    print("6. View All Cars")
    print("7. View Available Cars")
    print("8. Search Cars by Brand")
    print("\n👥 USER MANAGEMENT:")
    print("9. View All Users")
    print("10. Delete User")
    print("\n📊 SYSTEM:")
    print("11. System Statistics")
    print("12. Logout")
    print("0. Exit")

def handle_menu_choice(choice: str, menu_type: str) -> None:
    """
    Handle menu selection based on user type and choice.
    
    Args:
        choice: User's menu selection
        menu_type: Type of menu ("guest", "admin", "customer")
    """
    choices_dict = MENU_CHOICES.get(menu_type, {})
    
    if choice in choices_dict:
        choices_dict[choice]()
    else:
        print("❌ Invalid choice! Please select a valid option.")

if __name__ == "__main__":
    main()