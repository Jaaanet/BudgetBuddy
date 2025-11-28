# This module is showing the navigation menu and taking control on any user input response

# from __future__ import annotations
from typing import Dict
from budgetbuddy.core.models import UserProfile, Income, Expense
from budgetbuddy.data import repository
from budgetbuddy.ui import summary


class BudgetBuddyApp:
    """
    High-level controller:
        app = BudgetBuddyApp()
        app.run()
    """

    def __init__(self):
        self.profiles: Dict[str, UserProfile] = repository.load_profiles()
        self.current_month = 1
        self.current_year = 2025

    # 
    def run(self) -> None:
        """Start the main menu loop."""
        while True:
            choice = self._main_menu()
            if choice == "1":
                self.show_guide()
            elif choice == "2":
                self.create_profile_flow()
            elif choice == "3":
                self.saved_profiles_menu()
            elif choice == "4":
                repository.save_profiles(self.profiles)
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")

    # ---------- main menu ----------

    def _main_menu(self) -> str:
        print("\n=== BudgetBuddy Main Menu ===")
        print("1) Guide")
        print("2) Create profile")
        print("3) Saved profiles")
        print("4) Quit")
        return input("Choose an option: ").strip()

    def show_guide(self) -> None:
        print("\n=== Guide ===")
        print("This program lets you track income and expenses")
        print("for multiple profiles (accounts).")
        print("Create a profile, open it, then add transactions")
        print("and view monthly summaries.\n")

    def create_profile_flow(self) -> None:
        name = input("Enter a name for the new profile: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        if name in self.profiles:
            print("A profile with that name already exists.")
            return
        repository.create_profile(self.profiles, name)
        repository.save_profiles(self.profiles)
        print(f"Profile '{name}' created.")

    # ---------- saved profiles menu ----------

    def saved_profiles_menu(self) -> None:
        while True:
            summary.print_profiles_list(self.profiles)
            print("\nOptions:")
            print("  o) Open a profile")
            print("  r) Rename a profile")
            print("  d) Delete a profile")
            print("  b) Back to main menu")
            choice = input("Choose an option: ").strip().lower()

            if choice == "b":
                return
            elif choice == "o":
                self._open_profile_flow()
            elif choice == "r":
                self._rename_profile_flow()
            elif choice == "d":
                self._delete_profile_flow()
            else:
                print("Invalid choice.")

    def _open_profile_flow(self) -> None:
        name = input("Enter profile name to open: ").strip()
        profile = self.profiles.get(name)
        if not profile:
            print("No such profile.")
            return
        self.profile_summary_loop(profile)

    def _rename_profile_flow(self) -> None:
        old = input("Profile name to rename: ").strip()
        if old not in self.profiles:
            print("No such profile.")
            return
        new = input("New name: ").strip()
        if not new:
            print("Name cannot be empty.")
            return
        repository.rename_profile(self.profiles, old, new)
        repository.save_profiles(self.profiles)
        print("Profile renamed.")

    def _delete_profile_flow(self) -> None:
        name = input("Profile name to delete: ").strip()
        if name not in self.profiles:
            print("No such profile.")
            return
        confirm = input(f"Delete '{name}'? (y/n): ").strip().lower()
        if confirm == "y":
            repository.delete_profile(self.profiles, name)
            repository.save_profiles(self.profiles)
            print("Deleted.")

    # ---------- profile summary & actions ----------

    def profile_summary_loop(self, profile: UserProfile) -> None:
        while True:
            summary.print_summary_page(profile, self.current_month, self.current_year)
            print("\nProfile menu:", profile.name)
            print("1) Record income")
            print("2) Record expense")
            print("3) View all transactions this month")
            print("4) Edit a transaction")
            print("5) Delete a transaction")
            print("6) Change month")
            print("7) Back to Saved profiles")
            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.record_income_flow(profile)
            elif choice == "2":
                self.record_expense_flow(profile)
            elif choice == "3":
                self.view_all_transactions_flow(profile)
            elif choice == "4":
                self.edit_transaction_flow(profile)
            elif choice == "5":
                self.delete_transaction_flow(profile)
            elif choice == "6":
                self.change_month_flow()
            elif choice == "7":
                repository.save_profiles(self.profiles)
                return
            else:
                print("Invalid choice.")

    def record_income_flow(self, profile: UserProfile) -> None:
        date = input("Date (YYYY-MM-DD): ").strip()
        amount = float(input("Amount: "))
        category = input("Source/category: ").strip()
        desc = input("Description (optional): ").strip()
        tx = Income(date=date, amount=amount, category=category, description=desc)
        profile.add_transaction(tx)

    def record_expense_flow(self, profile: UserProfile) -> None:
        date = input("Date (YYYY-MM-DD): ").strip()
        amount = float(input("Amount: "))
        category = input("Category: ").strip()
        desc = input("Description (optional): ").strip()
        tx = Expense(date=date, amount=amount, category=category, description=desc)
        profile.add_transaction(tx)

    def view_all_transactions_flow(self, profile: UserProfile) -> None:
        txs = profile.list_transactions(self.current_month, self.current_year)
        print()
        summary.print_transactions(txs)

    def edit_transaction_flow(self, profile: UserProfile) -> None:
        txs = profile.list_transactions(self.current_month, self.current_year)
        summary.print_transactions(txs)
        if not txs:
            return
        try:
            index = int(input("Index of transaction to edit: "))
        except ValueError:
            print("Invalid index.")
            return
        if not (0 <= index < len(txs)):
            print("Index out of range.")
            return
        t = txs[index]
        print("Leave blank to keep existing value.")
        new_date = input(f"Date [{t.date}]: ").strip() or t.date
        new_amount_str = input(f"Amount [{t.amount}]: ").strip()
        new_amount = float(new_amount_str) if new_amount_str else t.amount
        new_cat = input(f"Category [{t.category}]: ").strip() or t.category
        new_desc = input(f"Description [{t.description}]: ").strip() or t.description
        t.date = new_date
        t.amount = new_amount
        t.category = new_cat
        t.description = new_desc

    def delete_transaction_flow(self, profile: UserProfile) -> None:
        txs = profile.list_transactions(self.current_month, self.current_year)
        summary.print_transactions(txs)
        if not txs:
            return
        try:
            index = int(input("Index of transaction to delete: "))
        except ValueError:
            print("Invalid index.")
            return
        if not (0 <= index < len(txs)):
            print("Index out of range.")
            return
        target = txs[index]
        profile.delete_transaction(target)

    def change_month_flow(self) -> None:
        year = input(f"Year [{self.current_year}]: ").strip()
        month = input(f"Month (1-12) [{self.current_month}]: ").strip()
        if year:
            self.current_year = int(year)
        if month:
            m = int(month)
            if 1 <= m <= 12:
                self.current_month = m
            else:
                print("Invalid month.")
    
def run() -> None:
        """Convenience function to start the BudgetBuddy program."""
        app = BudgetBuddyApp()
        app.run()
