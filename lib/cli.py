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
    print("5. View All Cars")
    print("6. View Available Cars")
    print("7. Search Cars by Brand")
    print("\n👥 USER MANAGEMENT:")
    print("8. View All Users")
    print("9. Delete User")
    print("\n📊 SYSTEM:")
    print("10. System Statistics")
    print("11. Logout")
    print("0. Exit")

def handle_menu_choice(choice):
    """Handle menu selection based on user type and choice"""
    if not current_user:  # Guest menu
        guest_choices = {
            "1": authenticate_user,
            "2": register_user,
            "3": list_available_cars,
            "4": search_cars_by_brand,
            "5": list_dealerships,
            "6": display_stats,
            "0": exit_program
        }
        
        if choice in guest_choices:
            guest_choices[choice]()
        else:
            print("❌ Invalid choice! Please select a valid option.")
    
    elif current_user.is_admin:  # Admin menu
        admin_choices = {
            "1": create_dealership,
            "2": view_my_dealerships,
            "3": list_dealerships,
            "4": delete_dealership,
            "5": list_all_cars,
            "6": list_available_cars,
            "7": search_cars_by_brand,
            "8": list_all_users,
            "9": delete_user,
            "10": display_stats,
            "11": logout_user,
            "0": exit_program
        }
        
        if choice in admin_choices:
            admin_choices[choice]()
        else:
            print("❌ Invalid choice! Please select a valid option.")
    
    else:  # Customer menu
        customer_choices = {
            "1": list_available_cars,
            "2": search_cars_by_brand,
            "3": purchase_car,
            "4": view_my_purchases,
            "5": list_dealerships,
            "6": display_stats,
            "7": logout_user,
            "0": exit_program
        }
        
        if choice in customer_choices:
            customer_choices[choice]()
        else:
            print("❌ Invalid choice! Please select a valid option.")

if __name__ == "__main__":
    main()