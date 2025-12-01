BudgetBuddy — Personal Budget Tracking CLI Application

BudgetBuddy is a simple text-based Python package for tracking personal income and expenses using named profiles (accounts).
It provides an easy way to record transactions, view yearly summaries, explore monthly totals, and manage multiple profiles — all through a clean command-line interface.

✨ Features
✔ Profile Management

Create, rename, delete, and open profiles (accounts)

Each profile stores its own set of transactions

Profiles are saved automatically in budgetbuddy_data.json

✔ Recording Transactions

Record income (salary, gifts, refunds, bonuses, etc.)

Record expenses (food, rent, entertainment, etc.)

Each transaction includes:

date (YYYY-MM-DD)

amount

category

optional description

✔ Yearly Views

View all transactions for the current year

Edit or delete transactions through a submenu

Change the selected year at any time

✔ Monthly Summaries

Generate a full summary such as:

=== Summary for janet (2025) ===

January
Total income : 500.00
Total expense: 200.00

February
Total income : 400.00
Total expense: 180.00
...

✔ Help Guide (External File)

guide.txt stored inside the ui/ folder

Loaded with a safe relative path

Easy to modify without touching code

📦 Package Structure
budgetbuddy/
    __init__.py          # exposes budgetbuddy.run()
    
    core/
        __init__.py
        models.py        # UserProfile, Transaction, Income, Expense
        budget.py        # Month totals, calculations, helpers
    
    data/
        __init__.py
        repository.py    # load/save JSON, manage profile storage
        csvio.py         # (optional) CSV import/export
    
    ui/
        __init__.py
        main.py          # CLI menus and program controller
        summary.py       # pretty-printed text summaries and listings
        guide.txt        # help/guide text displayed in the menu


The program stores all profile data in:

budgetbuddy_data.json


in the same directory from which the program is run.

▶️ Running the Program

Create a small runner script (example):

import budgetbuddy
budgetbuddy.run()


Save it as:

test.py


Run:

python test.py

📁 Data Storage

BudgetBuddy automatically creates and updates:

budgetbuddy_data.json


This file contains all saved profiles and transactions.
Make sure it remains in the same directory as your runner script.

🧩 Main User Interface (Profile Menu)

When you open a profile, you will see:

Profile menu for 'janet':
1) Record income
2) Record expense
3) View all transactions this year (2025)
4) Change year
5) View monthly summaries for this year (2025)
6) Back to Saved profiles


Option 3 opens a submenu:

[0] 2025-03-15 | Expense | 35.00 | Food | Lunch
[1] 2025-03-17 | Income  | 120.00 | Gift | Birthday

Options: e = edit, d = delete, b = back

🛠 Installation / Requirements

BudgetBuddy requires Python 3.8+.

Install required packages:

pip install -r requirements.txt


Typical dependencies:

json (built-in)
os (built-in)
pathlib (built-in)


BudgetBuddy uses only standard Python libraries, so installation is simple.

🎯 Purpose and Learning Goals

BudgetBuddy was developed as an educational project to practice:

Multi-file Python package structure

Data persistence using JSON

CLI application design

Object-oriented programming (OOP)

Clean separation between:

domain logic (core)

data storage (data)

user interface (ui)

📝 License

This project is for educational use in a software development course.
You may modify and adapt it for personal learning.

🙌 Credits

Developed by Janet Lu and team as part of a graduate-level Software Development course.
