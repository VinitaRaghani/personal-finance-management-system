import tkinter as tk
from tkinter import ttk
import re
from datetime import datetime  # Importing datetime for date validation
from db_manager import create_transaction_table, add_transaction, get_all_transactions
from report_generator import get_total_income_expense, visualize_expenses_by_category

# Initialize the database and create the transaction table
db_path = "finance.db"  # Define the path to your database
create_transaction_table(db_path)  # Pass the db_path here

import tkinter as tk
from tkinter import ttk
import re
from datetime import datetime  # Importing datetime for date validation

def submit_transaction(date_entry, category_entry, description_entry, amount_entry, trans_type, tab):
    """Submit the new transaction and display confirmation in the tab."""
    date = date_entry.get()
    category = category_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()

    # Date validation: Ensure it follows the format YYYY-MM-DD
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        error_label = tk.Label(tab, text="Date must be in YYYY-MM-DD format.", fg="red")
        error_label.pack()
        return

    # Check if the date is a valid calendar date and does not exceed today's date
    try:
        entered_date = datetime.strptime(date, "%Y-%m-%d")  # Convert to datetime
        today = datetime.today()  # Get today's date

        if entered_date > today:
            error_label = tk.Label(tab, text="Date cannot be in the future.", fg="red")
            error_label.pack()
            return
    except ValueError:
        error_label = tk.Label(tab, text="Invalid date. Please enter a valid date.", fg="red")
        error_label.pack()
        return

    if not category or not description or not amount:
        error_label = tk.Label(tab, text="Please fill in all fields.", fg="red")
        error_label.pack()
        return

    try:
        # Add transaction to the database
        add_transaction(date, category, description, float(amount), trans_type)
        success_label = tk.Label(tab, text="Transaction added successfully!", fg="green")
        success_label.pack()
    except Exception as e:
        error_label = tk.Label(tab, text=f"An error occurred: {e}", fg="red")
        error_label.pack()


def create_add_transaction_tab(tab):
    """Create the 'Add Transaction' tab with income and expense sub-tabs."""
    # Create a frame for the tab titles
    tab_titles_frame = tk.Frame(tab)
    tab_titles_frame.pack(pady=10)  # Use pack to position the frame

    # Create a Notebook for sub-tabs
    sub_notebook = ttk.Notebook(tab)
    sub_notebook.pack(pady=10, expand=True, fill="both")

    # Create Income tab
    tab_income = ttk.Frame(sub_notebook)
    sub_notebook.add(tab_income, text="Income")

    # Create Expense tab
    tab_expense = ttk.Frame(sub_notebook)
    sub_notebook.add(tab_expense, text="Expense")

    # Create buttons for Income and Expense
    income_button = tk.Button(tab_titles_frame, text="Income", command=lambda: sub_notebook.select(tab_income))
    expense_button = tk.Button(tab_titles_frame, text="Expense", command=lambda: sub_notebook.select(tab_expense))

    # Position the buttons in the frame
    income_button.grid(row=0, column=0, padx=(0, 50))  # Left side
    expense_button.grid(row=0, column=1)  # Right side

    # Create forms for income and expense
    create_income_form(tab_income)
    create_expense_form(tab_expense)

    # Optionally select the income tab by default
    sub_notebook.select(tab_income)

def create_income_form(tab):
    """Create the input form for adding income transactions."""
    tk.Label(tab, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=2, sticky="w")
    date_entry = tk.Entry(tab)
    date_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(tab, text="Category:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    category_entry = tk.Entry(tab)
    category_entry.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(tab, text="Description:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    description_entry = tk.Entry(tab)
    description_entry.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(tab, text="Amount:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
    amount_entry = tk.Entry(tab)
    amount_entry.grid(row=3, column=1, padx=5, pady=2)

    submit_button = tk.Button(tab, text="Add Income", command=lambda: submit_transaction(date_entry, category_entry, description_entry, amount_entry, "income", tab))
    submit_button.grid(row=4, column=0, padx=5, pady=10, sticky="e")  # Aligning the button to the right

def create_expense_form(tab):
    """Create the input form for adding expense transactions."""
    tk.Label(tab, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=2, sticky="w")
    date_entry = tk.Entry(tab)
    date_entry.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(tab, text="Category:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    category_entry = tk.Entry(tab)
    category_entry.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(tab, text="Description:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    description_entry = tk.Entry(tab)
    description_entry.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(tab, text="Amount:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
    amount_entry = tk.Entry(tab)
    amount_entry.grid(row=3, column=1, padx=5, pady=2)

    submit_button = tk.Button(tab, text="Add Expense", command=lambda: submit_transaction(date_entry, category_entry, description_entry, amount_entry, "expense", tab))
    submit_button.grid(row=4, column=1, padx=5, pady=10, sticky="w")  # Aligning the button to the left



def show_total_income_expense(tab):
    """Show total income and expenses within the tab."""
    total_income, total_expenses = get_total_income_expense(db_path)
    result_text = f"Total Income: ${total_income:.2f}\nTotal Expenses: ${total_expenses:.2f}"
    result_label = tk.Label(tab, text=result_text)
    result_label.pack()

def show_expenses_by_category(tab):
    """Visualize expenses by category within the tab."""
    result_text = visualize_expenses_by_category(db_path)  # Adjust this if necessary
    result_label = tk.Label(tab, text=result_text)
    result_label.pack()

def show_all_transactions(tab):
    """Display all transactions in the tab."""
    transactions = get_all_transactions(db_path)
    transactions_text = "\n".join(transactions) if transactions else "No transactions found."
    result_label = tk.Label(tab, text=transactions_text)
    result_label.pack()

# Function to handle tab switching event
def on_tab_changed(event):
    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")

    # Clear previous content in the tab (if any)
    for widget in event.widget.nametowidget(selected_tab).winfo_children():
        widget.destroy()

    if tab_text == "Add Transaction":
        create_add_transaction_tab(event.widget.nametowidget(selected_tab))
    elif tab_text == "Income & Expenses":
        show_total_income_expense(event.widget.nametowidget(selected_tab))
    elif tab_text == "Expenses by Category":
        show_expenses_by_category(event.widget.nametowidget(selected_tab))
    elif tab_text == "View All Transactions":
        show_all_transactions(event.widget.nametowidget(selected_tab))

# Main application window
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Personal Finance Management System")

    # Create a Notebook for main tabs
    notebook = ttk.Notebook(root)
    notebook.pack(padx=10, pady=10, expand=True, fill="both")

    # Tab 1: Add Transaction
    tab_add_transaction = ttk.Frame(notebook)
    notebook.add(tab_add_transaction, text="Add Transaction")

    # Tab 2: Show Total Income and Expenses
    tab_total_income_expense = ttk.Frame(notebook)
    notebook.add(tab_total_income_expense, text="Income & Expenses")

    # Tab 3: Visualize Expenses by Category
    tab_expenses_by_category = ttk.Frame(notebook)
    notebook.add(tab_expenses_by_category, text="Expenses by Category")

    # Tab 4: View All Transactions
    tab_view_all_transactions = ttk.Frame(notebook)
    notebook.add(tab_view_all_transactions, text="View All Transactions")

    # Bind tab change event to handle switching
    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    # Initialize the first tab (Add Transaction)
    create_add_transaction_tab(tab_add_transaction)

    # Start the GUI event loop
    root.mainloop()
