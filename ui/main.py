from budgetbuddy.core.models import UserProfile, Income, Expense
from budgetbuddy.core.budget import Budget
from budgetbuddy.data import repository
from budgetbuddy.ui import summary
import os


MONTH_NAMES = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]


class BudgetBuddyApp:
    """Main controller for the BudgetBuddy program."""

    def __init__(self):
        # Load all saved profiles from the JSON file
        self.profiles = repository.load_profiles()
        # We keep both current month and current year for summaries
        self.current_month = 1
        self.current_year = 2025  # can be changed by the user

    # ===== Entry point =====

    def run(self):
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

    # ===== Main menu =====

    def _main_menu(self):
        print("\n=== BudgetBuddy Main Menu ===")
        print("1) Guide")
        print("2) Create profile")
        print("3) Saved profiles")
        print("4) Quit")
        return input("Choose an option: ").strip()

    def show_guide(self):
        """Read guide.txt stored in the same directory as main.py."""
    # Determine the folder where main.py is located
        current_dir = os.path.dirname(__file__)  
    
    # Construct the path to guide.txt inside the same directory
        guide_path = os.path.join(current_dir, "guide.txt")

        try:
            with open(guide_path, "r", encoding="utf-8") as f:
                print("\n" + f.read())
        except FileNotFoundError:
            print("\nGuide file not found. Make sure guide.txt exists in the ui folder.")

    def create_profile_flow(self):
        name = input("Enter a name for the new profile: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        if name in self.profiles:
            print("A profile with that name already exists.")
            return

        repository.create_profile(self.profiles, name)
        repository.save_profiles(self.profiles)
        print("Profile '{}' created.".format(name))

    # ===== Saved profiles menu =====

    def saved_profiles_menu(self):
        while True:
            summary.print_profiles_list(self.profiles)
            print("\nOptions: o = open, r = rename, d = delete, b = back")
            choice = input("Choose: ").strip().lower()

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

    def _open_profile_flow(self):
        name = input("Profile name to open: ").strip()
        profile = self.profiles.get(name)
        if profile is None:
            print("No such profile.")
            return
        self.profile_summary_loop(profile)

    def _rename_profile_flow(self):
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

    def _delete_profile_flow(self):
        name = input("Profile name to delete: ").strip()
        if name not in self.profiles:
            print("No such profile.")
            return
        confirm = input("Delete '{}'? (y/n): ".format(name)).strip().lower()
        if confirm == "y":
            repository.delete_profile(self.profiles, name)
            repository.save_profiles(self.profiles)
            print("Deleted.")

    # ===== Profile summary and actions =====

    def profile_summary_loop(self, profile):
        """
        Menu shown after opening a profile.

        Now the menu is:

        1) Record income
        2) Record expense
        3) View all transactions this year (current_year)
        4) Edit a transaction
        5) Delete a transaction
        6) Change year
        7) View monthly summaries for this year (current_year)
        8) Back to Saved profiles
        """
        while True:
            # Summary page still shows totals for (current_month, current_year)
            summary.print_summary_page(profile, self.current_month, self.current_year)

            print("\nProfile menu for '{}':".format(profile.name))
            print("1) Record income")
            print("2) Record expense")
            print("3) View all transactions this year ({})".format(self.current_year))
            print("4) Edit a transaction")
            print("5) Delete a transaction")
            print("6) Change year")
            print("7) View monthly summaries for this year ({})".format(self.current_year))
            print("8) Back to Saved profiles")

            choice = input("Choose: ").strip()

            if choice == "1":
                self.record_income_flow(profile)
            elif choice == "2":
                self.record_expense_flow(profile)
            elif choice == "3":
                self.view_year_transactions_flow(profile)
            elif choice == "4":
                self.edit_transaction_flow(profile)
            elif choice == "5":
                self.delete_transaction_flow(profile)
            elif choice == "6":
                self.change_year_flow()
            elif choice == "7":
                self.view_monthly_summaries_flow(profile)
            elif choice == "8":
                repository.save_profiles(self.profiles)
                return
            else:
                print("Invalid choice.")

    def record_income_flow(self, profile):
        date = input("Date (YYYY-MM-DD): ").strip()
        amount = float(input("Amount: "))
        category = input("Source/category: ").strip()
        desc = input("Description (optional): ").strip()
        tx = Income(date, amount, category, desc)
        profile.add_transactions(tx)

    def record_expense_flow(self, profile):
        date = input("Date (YYYY-MM-DD): ").strip()
        amount = float(input("Amount: "))
        category = input("Category: ").strip()
        desc = input("Description (optional): ").strip()
        tx = Expense(date, amount, category, desc)
        profile.add_transactions(tx)

    # === View all transactions for the current year ===

    def view_year_transactions_flow(self, profile):
        """Show all transactions in the current year for this profile."""
        prefix = "{:04d}-".format(self.current_year)  # matches "YYYY-"
        txs = []
        for t in profile.transactions:
            if isinstance(t.date, str) and t.date.startswith(prefix):
                txs.append(t)

        print()
        summary.print_transactions(txs)

    # === NEW: View monthly summaries for the current year ===

    def view_monthly_summaries_flow(self, profile):
        """Print income and expense totals for each month of the current year."""
        budget = Budget(profile)
        year = self.current_year

        print("\n=== Summary for {} ({}) ===".format(profile.name, year))

        for month in range(1, 13):
            totals = budget.month_totals(month, year)
            month_name = MONTH_NAMES[month - 1]

            print("\n{}".format(month_name))
            print("Total income : {:.2f}".format(totals["income"]))
            print("Total expense: {:.2f}".format(totals["expense"]))

    def edit_transaction_flow(self, profile):
        # Still editing only the current month/year subset
        txs = profile.list_transactions(self.current_month, self.current_year)
        summary.print_transactions(txs)
        if not txs:
            return

        try:
            index = int(input("Index of transaction to edit: "))
        except ValueError:
            print("Invalid index.")
            return

        if index < 0 or index >= len(txs):
            print("Index out of range.")
            return

        t = txs[index]
        print("Leave blank to keep existing value.")
        new_date = input("Date [{}]: ".format(t.date)).strip()
        new_amount = input("Amount [{}]: ".format(t.amount)).strip()
        new_cat = input("Category [{}]: ".format(t.category)).strip()
        new_desc = input("Description [{}]: ".format(t.description)).strip()

        if new_date:
            t.date = new_date
        if new_amount:
            t.amount = float(new_amount)
        if new_cat:
            t.category = new_cat
        if new_desc:
            t.description = new_desc

    def delete_transaction_flow(self, profile):
        txs = profile.list_transactions(self.current_month, self.current_year)
        summary.print_transactions(txs)
        if not txs:
            return

        try:
            index = int(input("Index of transaction to delete: "))
        except ValueError:
            print("Invalid index.")
            return

        if index < 0 or index >= len(txs):
            print("Index out of range.")
            return

        target = txs[index]
        profile.delete_transaction(target)
        print("Transaction deleted.")

    # === Change year (keeps month as-is) ===

    def change_year_flow(self):
        """Allow the user to change the current year."""
        new_year = input("Year [{}]: ".format(self.current_year)).strip()
        if new_year:
            try:
                self.current_year = int(new_year)
                print("Year changed to {}.".format(self.current_year))
            except ValueError:
                print("Invalid year. Please enter a number.")


def run():
    """Helper so we can call budgetbuddy.run()."""
    app = BudgetBuddyApp()
    app.run()
