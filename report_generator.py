import sqlite3
import matplotlib.pyplot as plt

def generate_report(db_path):
    """
    Generates a financial report based on the data in the SQLite database.

    Args:
        db_path (str): The path to the SQLite database file.

    Returns:
        dict: A summary report containing total income, total expenses, and balance.
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Calculate total income
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
    total_income = cursor.fetchone()[0] or 0

    # Calculate total expenses
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
    total_expenses = cursor.fetchone()[0] or 0

    # Calculate balance
    balance = total_income - total_expenses

    # Close the database connection
    conn.close()

    # Create the report
    report = {
        'Total Income': total_income,
        'Total Expenses': total_expenses,
        'Balance': balance
    }

    return report

def get_total_income_expense(db_path):
    """
    Gets the total income and expenses from the database.

    Args:
        db_path (str): The path to the SQLite database file.

    Returns:
        tuple: A tuple containing total income and total expenses.
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get total income
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
    total_income = cursor.fetchone()[0] or 0

    # Get total expenses
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
    total_expenses = cursor.fetchone()[0] or 0

    # Close the database connection
    conn.close()

    return total_income, total_expenses

def visualize_expenses_by_category(db_path):
    """
    Visualizes expenses by category using a pie chart.

    Args:
        db_path (str): The path to the SQLite database file.
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get the total expenses by category
    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE type = 'expense'
        GROUP BY category
    """)
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Prepare data for pie chart
    categories = [row[0] for row in data]
    expenses = [row[1] for row in data]

    # Create pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(expenses, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expenses by Category')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

if __name__ == "__main__":
    # Example usage
    db_path = "finance.db"  # Update this path as necessary

    # Generate and print the report
    report = generate_report(db_path)
    print("Financial Report:")
    for key, value in report.items():
        print(f"{key}: ${value:.2f}")

    # Visualize expenses by category
    visualize_expenses_by_category(db_path)
