import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import tkinter as tk

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


def visualize_expenses_by_category(parent, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get total expenses
    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE type = 'expense'
    """)
    total_expenses = cursor.fetchone()[0] or 0  # Default to 0 if None

    # Get total income
    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE type = 'income'
    """)
    total_income = cursor.fetchone()[0] or 0  # Default to 0 if None

    # Display KPI Cards
    kpi_frame = tk.Frame(parent)
    kpi_frame.pack(pady=10)

    tk.Label(kpi_frame, text=f"Total Income: ${total_income:.2f}", font=("Arial", 12)).grid(row=0, column=0, padx=10)
    tk.Label(kpi_frame, text=f"Total Expenses: ${total_expenses:.2f}", font=("Arial", 12)).grid(row=0, column=1, padx=10)

    # Get expenses and income by month
    cursor.execute("""
        SELECT strftime('%Y-%m', date) as month_year, 
               SUM(CASE WHEN type='income' THEN amount ELSE 0 END) AS total_income,
               SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) AS total_expenses
        FROM transactions
        GROUP BY month_year
        ORDER BY month_year
    """)
    monthly_data = cursor.fetchall()

    months = [row[0] for row in monthly_data]
    income_values = [row[1] for row in monthly_data]
    expense_values = [row[2] for row in monthly_data]

    # Create clustered bar chart for income and expenses
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.35  # Width of the bars
    x = range(len(months))  # X-axis positions

    ax.bar([i - width / 2 for i in x], income_values, width, label='Income', color='lightgreen')
    ax.bar([i + width / 2 for i in x], expense_values, width, label='Expenses', color='lightcoral')

    ax.set_title('Monthly Income and Expenses')
    ax.set_ylabel('Amount')
    ax.set_xlabel('Month-Year')
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45)
    ax.legend()

    # Display the chart in the Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Bar Charts: Expenditures by Category and Subcategory
    cursor.execute("""
        SELECT category, subcategory, SUM(amount)
        FROM transactions
        WHERE type = 'expense'
        GROUP BY category, subcategory
    """)
    category_data = cursor.fetchall()

    categories = list(set(row[0] for row in category_data))
    subcategories = [row[1] for row in category_data]
    expenditures = [row[2] for row in category_data]

    # Create bar chart for expenditures by category and subcategory
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.bar(subcategories, expenditures, color='skyblue')

    ax2.set_title('Expenditures by Category and Subcategory')
    ax2.set_ylabel('Amount')
    ax2.set_xlabel('Subcategory')
    ax2.set_xticklabels(subcategories, rotation=45)

    canvas2 = FigureCanvasTkAgg(fig2, master=parent)
    canvas2.draw()
    canvas2.get_tk_widget().pack()

    # Pie Charts: Proportional Spending by Category
    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE type = 'expense'
        GROUP BY category
    """)
    pie_data = cursor.fetchall()

    pie_categories = [row[0] for row in pie_data]
    pie_expenses = [row[1] for row in pie_data]

    # Create pie chart for spending proportions
    fig3, ax3 = plt.subplots(figsize=(8, 8))
    ax3.pie(pie_expenses, labels=pie_categories, autopct='%1.1f%%', startangle=140)
    ax3.set_title('Proportional Spending by Category')

    canvas3 = FigureCanvasTkAgg(fig3, master=parent)
    canvas3.draw()
    canvas3.get_tk_widget().pack()

    conn.close()