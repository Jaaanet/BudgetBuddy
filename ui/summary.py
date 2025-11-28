from budgetbuddy.core.budget import Budget


def print_summary_page(profile, month, year):
    """Print the summary page for a profile and month."""
    budget = Budget(profile)
    totals = budget.month_totals(month, year)
    recent = budget.recent_transactions(month, year)

    print("\n=== Summary for {} ({}-{:02d}) ===".format(profile.name, year, month))
    print("Total income : {:.2f}".format(totals["income"]))
    print("Total expense: {:.2f}".format(totals["expense"]))
    print("Net balance  : {:.2f}".format(totals["net"]))
    print("\nRecent transactions:")
    print_transactions(recent)


def print_transactions(transactions):
    """Pretty-print a list of transactions."""
    if not transactions:
        print("  (no transactions)")
        return

    for i, t in enumerate(transactions):
        line = "[{}] {} | {:7} | {:10} | {:8.2f} | {}".format(
            i,
            t.date,
            t.get_type(),
            t.category,
            t.amount,
            t.description,
        )
        print(line)


def print_profiles_list(profiles):
    """Print all saved profile names."""
    print("\n=== Saved profiles ===")
    if not profiles:
        print("  (no profiles yet)")
        return
    for i, name in enumerate(profiles.keys()):
        print("[{}] {}".format(i, name))
