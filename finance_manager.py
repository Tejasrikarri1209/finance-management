import sqlite3
import os
import shutil
from datetime import datetime
from hashlib import sha256

# Connect to the database (or create it if it doesn’t exist)
conn = sqlite3.connect('finance_app.db')
cursor = conn.cursor()

# Create a users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
''')
conn.commit()
def register_user(username, password):
    # Hash the password
    password_hash = sha256(password.encode()).hexdigest()
    
    # Store user in the database
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already taken. Please choose a different username.")
def login_user(username, password):
    # Hash the password to compare with stored hash
    password_hash = sha256(password.encode()).hexdigest()
    
    # Fetch the user's stored hash
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    
    if result and result[0] == password_hash:
        print("Login successful!")
        return True
    else:
        print("Invalid username or password. Please try again.")
        return False
def main():
    while True:
        print("1. Register")
        print("2. Login")
        choice = input("Select an option (1 or 2): ")
        
        if choice == '1':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            register_user(username, password)
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if login_user(username, password):
                print("Welcome to your Personal Finance Manager!")
                break
        else:
            print("Invalid choice. Please select again.")

#1
main()


# Database setup
conn = sqlite3.connect('finance_manager.db')
cursor = conn.cursor()

# Create tables for transactions
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,          -- 'income' or 'expense'
        category TEXT NOT NULL,      -- e.g., Food, Rent, Salary
        amount REAL NOT NULL,
        date TEXT NOT NULL,          -- ISO format YYYY-MM-DD
        description TEXT
    )
''')
conn.commit()

# Function to add a transaction
def add_transaction():
    print("\nAdd Transaction")
    trans_type = input("Enter type (income/expense): ").strip().lower()
    if trans_type not in ['income', 'expense']:
        print("Invalid type. Please enter 'income' or 'expense'.")
        return

    category = input("Enter category (e.g., Food, Rent, Salary): ").strip()
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    description = input("Enter description (optional): ").strip()
    date = input("Enter date (YYYY-MM-DD, leave blank for today): ").strip() or datetime.now().strftime('%Y-%m-%d')

    try:
        datetime.strptime(date, '%Y-%m-%d')  # Validate date
        cursor.execute('''
            INSERT INTO transactions (type, category, amount, date, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (trans_type, category, amount, date, description))
        conn.commit()
        print("Transaction added successfully.")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")

# Function to update a transaction
def update_transaction():
    print("\nUpdate Transaction")
    trans_id = input("Enter transaction ID to update: ").strip()
    cursor.execute("SELECT * FROM transactions WHERE id = ?", (trans_id,))
    transaction = cursor.fetchone()
    if not transaction:
        print("Transaction not found.")
        return

    print("Leave fields blank to keep the current value.")
    new_type = input(f"Type (current: {transaction[1]}): ").strip() or transaction[1]
    if new_type not in ['income', 'expense']:
        print("Invalid type.")
        return

    new_category = input(f"Category (current: {transaction[2]}): ").strip() or transaction[2]
    try:
        new_amount = float(input(f"Amount (current: {transaction[3]}): ").strip() or transaction[3])
    except ValueError:
        print("Invalid amount.")
        return

    new_description = input(f"Description (current: {transaction[5]}): ").strip() or transaction[5]
    new_date = input(f"Date (current: {transaction[4]}): ").strip() or transaction[4]

    try:
        datetime.strptime(new_date, '%Y-%m-%d')  # Validate date
        cursor.execute('''
            UPDATE transactions
            SET type = ?, category = ?, amount = ?, date = ?, description = ?
            WHERE id = ?
        ''', (new_type, new_category, new_amount, new_date, new_description, trans_id))
        conn.commit()
        print("Transaction updated successfully.")
    except ValueError:
        print("Invalid date format.")

# Function to delete a transaction
def delete_transaction():
    print("\nDelete Transaction")
    trans_id = input("Enter transaction ID to delete: ").strip()
    cursor.execute("SELECT * FROM transactions WHERE id = ?", (trans_id,))
    if not cursor.fetchone():
        print("Transaction not found.")
        return

    cursor.execute("DELETE FROM transactions WHERE id = ?", (trans_id,))
    conn.commit()
    print("Transaction deleted successfully.")

# Function to view all transactions
def view_transactions():
    print("\nView Transactions")
    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    transactions = cursor.fetchall()
    if not transactions:
        print("No transactions found.")
        return

    print("{:<5} {:<10} {:<15} {:<10} {:<12} {}".format("ID", "Type", "Category", "Amount", "Date", "Description"))
    print("-" * 70)
    for trans in transactions:
        print(f"{trans[0]:<5} {trans[1]:<10} {trans[2]:<15} {trans[3]:<10.2f} {trans[4]:<12} {trans[5]}")

# Menu-driven interface
def main():
    while True:
        print("\nPersonal Finance Manager")
        print("1. Add Transaction")
        print("2. Update Transaction")
        print("3. Delete Transaction")
        print("4. View Transactions")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_transaction()
        elif choice == '2':
            update_transaction()
        elif choice == '3':
            delete_transaction()
        elif choice == '4':
            view_transactions()
        elif choice == '5':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

#2
if __name__ == "__main__":
    main()


# Database setup
conn = sqlite3.connect('finance_manager.db')
cursor = conn.cursor()

# Ensure the transactions table exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,          -- 'income' or 'expense'
        category TEXT NOT NULL,      -- e.g., Food, Rent, Salary
        amount REAL NOT NULL,
        date TEXT NOT NULL           -- ISO format YYYY-MM-DD
    )
''')
conn.commit()

# Function to generate a monthly report
def generate_monthly_report():
    print("\nGenerate Monthly Report")
    year = input("Enter year (YYYY): ").strip()
    month = input("Enter month (MM): ").strip()

    try:
        datetime.strptime(f"{year}-{month}-01", '%Y-%m-%d')  # Validate year and month
    except ValueError:
        print("Invalid date. Please enter a valid year and month.")
        return

    cursor.execute('''
        SELECT type, SUM(amount) 
        FROM transactions 
        WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
        GROUP BY type
    ''', (year, month))

    results = cursor.fetchall()
    if not results:
        print("No transactions found for the specified month.")
        return

    total_income = sum(amount for ttype, amount in results if ttype == 'income')
    total_expenses = sum(amount for ttype, amount in results if ttype == 'expense')
    savings = total_income - total_expenses

    print(f"\nMonthly Report for {year}-{month}")
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Savings: ${savings:.2f}")

# Function to generate a yearly report
def generate_yearly_report():
    print("\nGenerate Yearly Report")
    year = input("Enter year (YYYY): ").strip()

    try:
        datetime.strptime(f"{year}-01-01", '%Y-%m-%d')  # Validate year
    except ValueError:
        print("Invalid year. Please enter a valid year.")
        return

    cursor.execute('''
        SELECT type, SUM(amount) 
        FROM transactions 
        WHERE strftime('%Y', date) = ?
        GROUP BY type
    ''', (year,))

    results = cursor.fetchall()
    if not results:
        print("No transactions found for the specified year.")
        return

    total_income = sum(amount for ttype, amount in results if ttype == 'income')
    total_expenses = sum(amount for ttype, amount in results if ttype == 'expense')
    savings = total_income - total_expenses

    print(f"\nYearly Report for {year}")
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Savings: ${savings:.2f}")

# Function to add a transaction (for testing and demonstration purposes)
def add_transaction():
    print("\nAdd Transaction")
    trans_type = input("Enter type (income/expense): ").strip().lower()
    if trans_type not in ['income', 'expense']:
        print("Invalid type. Please enter 'income' or 'expense'.")
        return

    category = input("Enter category (e.g., Food, Rent, Salary): ").strip()
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    date = input("Enter date (YYYY-MM-DD, leave blank for today): ").strip() or datetime.now().strftime('%Y-%m-%d')

    try:
        datetime.strptime(date, '%Y-%m-%d')  # Validate date
        cursor.execute('''
            INSERT INTO transactions (type, category, amount, date)
            VALUES (?, ?, ?, ?)
        ''', (trans_type, category, amount, date))
        conn.commit()
        print("Transaction added successfully.")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")

# Menu-driven interface
def main():
    while True:
        print("\nPersonal Finance Manager")
        print("1. Add Transaction")
        print("2. Generate Monthly Report")
        print("3. Generate Yearly Report")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_transaction()
        elif choice == '2':
            generate_monthly_report()
        elif choice == '3':
            generate_yearly_report()
        elif choice == '4':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

#3
if __name__ == "__main__":
    main()


# Database setup
conn = sqlite3.connect('finance_manager.db')
cursor = conn.cursor()

# Ensure necessary tables exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,          -- 'income' or 'expense'
        category TEXT NOT NULL,      -- e.g., Food, Rent, Salary
        amount REAL NOT NULL,
        date TEXT NOT NULL           -- ISO format YYYY-MM-DD
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,      -- e.g., Food, Rent
        amount REAL NOT NULL,        -- Budget limit
        month TEXT NOT NULL,         -- Format: YYYY-MM
        UNIQUE(category, month)      -- Ensure one budget per category per month
    )
''')
conn.commit()

# Function to set a budget
def set_budget():
    print("\nSet Budget")
    category = input("Enter category (e.g., Food, Rent): ").strip()
    try:
        amount = float(input("Enter budget amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    month = input("Enter month (YYYY-MM, leave blank for current month): ").strip() or datetime.now().strftime('%Y-%m')

    try:
        datetime.strptime(month, '%Y-%m')  # Validate month format
        cursor.execute('''
            INSERT INTO budgets (category, amount, month)
            VALUES (?, ?, ?)
            ON CONFLICT(category, month) DO UPDATE SET amount = excluded.amount
        ''', (category, amount, month))
        conn.commit()
        print(f"Budget for '{category}' set to ${amount:.2f} for {month}.")
    except ValueError:
        print("Invalid month format. Please use YYYY-MM.")

# Function to add a transaction
def add_transaction():
    print("\nAdd Transaction")
    trans_type = input("Enter type (income/expense): ").strip().lower()
    if trans_type not in ['income', 'expense']:
        print("Invalid type. Please enter 'income' or 'expense'.")
        return

    category = input("Enter category (e.g., Food, Rent): ").strip()
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    date = input("Enter date (YYYY-MM-DD, leave blank for today): ").strip() or datetime.now().strftime('%Y-%m-%d')

    try:
        datetime.strptime(date, '%Y-%m-%d')  # Validate date
        cursor.execute('''
            INSERT INTO transactions (type, category, amount, date)
            VALUES (?, ?, ?, ?)
        ''', (trans_type, category, amount, date))
        conn.commit()
        print("Transaction added successfully.")
        check_budget_limit(category, amount, date)
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")

# Function to check budget limit for a category
def check_budget_limit(category, amount, date):
    if datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m') == datetime.now().strftime('%Y-%m'):
        month = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m')

        # Get total expenses for this category and month
        cursor.execute('''
            SELECT SUM(amount) 
            FROM transactions 
            WHERE category = ? AND type = 'expense' AND strftime('%Y-%m', date) = ?
        ''', (category, month))
        total_expenses = cursor.fetchone()[0] or 0

        # Get budget limit
        cursor.execute('''
            SELECT amount 
            FROM budgets 
            WHERE category = ? AND month = ?
        ''', (category, month))
        budget = cursor.fetchone()

        if budget:
            budget_limit = budget[0]
            if total_expenses > budget_limit:
                print(f"Warning: Budget exceeded for '{category}'!")
                print(f"Total Expenses: ${total_expenses:.2f}, Budget: ${budget_limit:.2f}")

# Function to view budgets
def view_budgets():
    print("\nView Budgets")
    month = input("Enter month to view budgets (YYYY-MM, leave blank for current month): ").strip() or datetime.now().strftime('%Y-%m')

    try:
        datetime.strptime(month, '%Y-%m')  # Validate month format
        cursor.execute('''
            SELECT category, amount 
            FROM budgets 
            WHERE month = ?
        ''', (month,))
        budgets = cursor.fetchall()

        if not budgets:
            print(f"No budgets set for {month}.")
            return

        print(f"\nBudgets for {month}:")
        print("{:<15} {:<10}".format("Category", "Budget"))
        print("-" * 25)
        for category, amount in budgets:
            print(f"{category:<15} ${amount:.2f}")
    except ValueError:
        print("Invalid month format. Please use YYYY-MM.")

# Menu-driven interface
def main():
    while True:
        print("\nPersonal Finance Manager - Budgeting")
        print("1. Set Budget")
        print("2. Add Transaction")
        print("3. View Budgets")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            set_budget()
        elif choice == '2':
            add_transaction()
        elif choice == '3':
            view_budgets()
        elif choice == '4':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

#5
if __name__ == "__main__":
    main()

# Database setup
DB_NAME = "finance_manager.db"

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,          -- 'income' or 'expense'
            category TEXT NOT NULL,      -- e.g., Food, Rent, Salary
            amount REAL NOT NULL,
            date TEXT NOT NULL           -- ISO format YYYY-MM-DD
        )
    ''')
    conn.commit()
    return conn

conn = setup_database()
cursor = conn.cursor()

# Add a transaction
def add_transaction():
    print("\nAdd Transaction")
    trans_type = input("Enter type (income/expense): ").strip().lower()
    if trans_type not in ['income', 'expense']:
        print("Invalid type. Please enter 'income' or 'expense'.")
        return

    category = input("Enter category (e.g., Food, Rent, Salary): ").strip()
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    date = input("Enter date (YYYY-MM-DD, leave blank for today): ").strip() or datetime.now().strftime('%Y-%m-%d')

    try:
        datetime.strptime(date, '%Y-%m-%d')  # Validate date
        cursor.execute('''
            INSERT INTO transactions (type, category, amount, date)
            VALUES (?, ?, ?, ?)
        ''', (trans_type, category, amount, date))
        conn.commit()
        print("Transaction added successfully.")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")

# View all transactions
def view_transactions():
    print("\nAll Transactions")
    cursor.execute('SELECT id, type, category, amount, date FROM transactions ORDER BY date')
    transactions = cursor.fetchall()

    if not transactions:
        print("No transactions found.")
        return

    print("{:<5} {:<10} {:<15} {:<10} {:<12}".format("ID", "Type", "Category", "Amount", "Date"))
    print("-" * 50)
    for trans in transactions:
        print("{:<5} {:<10} {:<15} {:<10.2f} {:<12}".format(*trans))

# Back up the database
def backup_data():
    print("\nBackup Data")
    backup_folder = "backups"
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    backup_file = os.path.join(backup_folder, f"{DB_NAME}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.backup")
    try:
        shutil.copy(DB_NAME, backup_file)
        print(f"Backup created at: {backup_file}")
    except Exception as e:
        print(f"Error during backup: {e}")

# Restore data from a backup
def restore_data():
    print("\nRestore Data")
    backup_folder = "backups"
    if not os.path.exists(backup_folder):
        print("No backups found.")
        return

    backups = [f for f in os.listdir(backup_folder) if f.endswith(".backup")]
    if not backups:
        print("No backup files available.")
        return

    print("\nAvailable Backups:")
    for idx, backup in enumerate(backups):
        print(f"{idx + 1}. {backup}")

    try:
        choice = int(input("Enter the number of the backup to restore: "))
        if 1 <= choice <= len(backups):
            backup_file = os.path.join(backup_folder, backups[choice - 1])
            shutil.copy(backup_file, DB_NAME)
            print(f"Database restored from: {backup_file}")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Menu-driven interface
def main():
    while True:
        print("\nPersonal Finance Manager - Data Persistence")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Backup Data")
        print("4. Restore Data")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            backup_data()
        elif choice == '4':
            restore_data()
        elif choice == '5':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

#6
if __name__ == "__main__":
    main()

DB_NAME = "finance_manager.db"

# Database setup
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn

conn = setup_database()
cursor = conn.cursor()

# Add a transaction
def add_transaction(trans_type, category, amount, date):
    if trans_type not in ['income', 'expense']:
        return "Invalid transaction type"
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return "Invalid date format"
    cursor.execute('''
        INSERT INTO transactions (type, category, amount, date)
        VALUES (?, ?, ?, ?)
    ''', (trans_type, category, amount, date))
    conn.commit()
    return "Transaction added successfully"

# View all transactions
def view_transactions():
    cursor.execute('SELECT type, category, amount, date FROM transactions ORDER BY date')
    return cursor.fetchall()

# Delete all transactions (utility for testing)
def delete_all_transactions():
    cursor.execute('DELETE FROM transactions')
    conn.commit()
import unittest
from finance_manager import add_transaction, view_transactions, delete_all_transactions

class TestFinanceManager(unittest.TestCase):

    def setUp(self):
        # Clear the database before each test
        delete_all_transactions()

    def test_add_transaction_success(self):
        result = add_transaction("income", "Salary", 5000, "2024-11-19")
        self.assertEqual(result, "Transaction added successfully")

    def test_add_transaction_invalid_type(self):
        result = add_transaction("investment", "Stocks", 1000, "2024-11-19")
        self.assertEqual(result, "Invalid transaction type")

    def test_add_transaction_invalid_date(self):
        result = add_transaction("expense", "Food", 100, "19-11-2024")
        self.assertEqual(result, "Invalid date format")

    def test_view_transactions(self):
        add_transaction("income", "Salary", 5000, "2024-11-19")
        add_transaction("expense", "Food", 100, "2024-11-20")
        transactions = view_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0], ("income", "Salary", 5000, "2024-11-19"))
        self.assertEqual(transactions[1], ("expense", "Food", 100, "2024-11-20"))

#7
if __name__ == "__main__":
    unittest.main()





