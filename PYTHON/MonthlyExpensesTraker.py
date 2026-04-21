import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"


def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])

def clean_text(text):
    return text.strip().replace("'", "").replace('"', "")


def add_expense():
    date = clean_text(input("Enter date (YYYY-MM-DD) or press Enter for today: "))
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    category = clean_text(input("Enter category (Food, Travel, Bills, etc.): "))

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount.\n")
        return

    description = clean_text(input("Enter description: "))

    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])

    print("Expense added successfully!\n")


def read_expenses():
    expenses = []

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                date = clean_text(row["Date"])
                amount = float(row["Amount"])

                expenses.append({
                    "date": date,
                    "category": clean_text(row["Category"]),
                    "amount": amount,
                    "description": clean_text(row["Description"])
                })
            except Exception:
                print(f"Skipping corrupted row: {row}")

    return expenses

def budget_insights(total, category_totals):
    print("\nBudget Analysis")

    try:
        budget = float(input("Enter your budget (₹): "))
    except ValueError:
        print("Invalid budget input.")
        return

    if total > budget:
        print(f"\nYou exceeded your budget by ₹{total - budget}")
    else:
        print(f"\nYou are within budget. Remaining: ₹{budget - total}")

    print("\nSmart Suggestions:")

    for category, amount in category_totals.items():
        percentage = (amount / total) * 100 if total > 0 else 0

        if percentage > 40:
            print(f"High spending on {category} ({percentage:.1f}%) - Try to reduce it.")
        elif percentage > 25:
            print(f"Moderate spending on {category} ({percentage:.1f}%) - Keep an eye on it.")
        else:
            print(f"{category} spending is under control ({percentage:.1f}%).")

def monthly_summary():
    month = input("Enter month (YYYY-MM): ")
    expenses = read_expenses()

    total = 0
    category_totals = {}

    for expense in expenses:
        if expense["date"].startswith(month):
            total += expense["amount"]
            category = expense["category"]
            category_totals[category] = category_totals.get(category, 0) + expense["amount"]

    print(f"\nTotal Expenses for {month}: ₹{total}")

    print("\nCategory-wise Breakdown:")
    for cat, amt in category_totals.items():
        print(f"{cat}: ₹{amt}")

    if category_totals:
        highest = max(category_totals, key=category_totals.get)
        print(f"\nHighest Spending Category: {highest} (₹{category_totals[highest]})")

        plt.figure()
        plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%')
        plt.title(f"Expense Distribution for {month}")
        plt.show()

    if total > 0:
        budget_insights(total, category_totals)

    input("\nPress Enter to return to menu...")

def date_range_history():
    print("\nView Expenses by Date Range")

    start_date = clean_text(input("Enter start date (YYYY-MM-DD): "))
    end_date = clean_text(input("Enter end date (YYYY-MM-DD): "))

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format!")
        return

    expenses = read_expenses()

    filtered = []
    total = 0
    category_totals = {}

    for expense in expenses:
        try:
            expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
        except ValueError:
            print(f"Skipping invalid date: {expense['date']}")
            continue

        if start <= expense_date <= end:
            filtered.append(expense)
            total += expense["amount"]

            category = expense["category"]
            category_totals[category] = category_totals.get(category, 0) + expense["amount"]

    if not filtered:
        print("No expenses found in this range.")
        input("\nPress Enter to return to menu...")
        return

    print(f"\nTotal Spending: ₹{total}")
    print("\nTransactions:")

    for exp in filtered:
        print(f"{exp['date']} | {exp['category']} | ₹{exp['amount']} | {exp['description']}")

    print("\nCategory-wise Summary:")
    for cat, amt in category_totals.items():
        print(f"{cat}: ₹{amt}")

    if total > 0:
        budget_insights(total, category_totals)

    input("\nPress Enter to return to menu...")


def menu():
    initialize_file()

    while True:
        print("\n==== Smart Expense Tracker ====")
        print("1. Add Expense")
        print("2. View Monthly Summary")
        print("3. View Date Range History")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            monthly_summary()
        elif choice == "3":
            date_range_history()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
