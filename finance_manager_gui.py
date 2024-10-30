import tkinter as tk
from tkinter import ttk
import re
from datetime import datetime 
from datetime import date
from db_manager import create_transaction_table, add_transaction, get_all_transactions
from report_generator import  visualize_expenses_by_category

# Initialize the database and create the transaction table
db_path = "finance.db"  # Define the path to your database
create_transaction_table(db_path)  # Pass the db_path here

def submit_transaction(date_combobox, month_combobox, year_combobox, category_entry, description_entry, amount_entry, trans_type, tab):
    """Submit the new transaction and display confirmation in the tab."""
    
    # Get the date components
    year = year_combobox.get()
    month = month_combobox.get()
    day = date_combobox.get()

    # Concatenate into a proper date string
    date = f"{year}-{month}-{day}"

    category = category_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()

    # Date validation: Ensure it follows the format YYYY-MM-DD
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        error_label = tk.Label(tab, text="Date must be in YYYY-MM-DD format.", fg="red")
        error_label.grid(row=5, column=0, columnspan=2, padx=5, pady=2, sticky="w")
        return

    # Check if the date is a valid calendar date and does not exceed today's date
    try:
        entered_date = datetime.strptime(date, "%Y-%m-%d")  # Convert to datetime
        today = datetime.today()  # Get today's date

        if entered_date > today:
            error_label = tk.Label(tab, text="Date cannot be in the future.", fg="red")
            error_label.grid(row=5, column=0, columnspan=2, padx=5, pady=2, sticky="w")
            return
    except ValueError:
        error_label = tk.Label(tab, text="Invalid date. Please enter a valid date.", fg="red")
        error_label.grid(row=5, column=0, columnspan=2, padx=5, pady=2, sticky="w")
        return

    if not category or not description or not amount:
        error_label = tk.Label(tab, text="Please fill in all fields.", fg="red")
        error_label.grid(row=5, column=0, columnspan=2, padx=5, pady=2, sticky="w")
        return

    try:
        # Add transaction to the database
        add_transaction(date, category, description, float(amount), trans_type)
        success_label = tk.Label(tab, text="Transaction added successfully!", fg="green")
        success_label.grid(row=5, column=0, columnspan=2, padx=5, pady=2, sticky="w")

        # Reset input fields
        year_combobox.set("yyyy")
        month_combobox.set("mm")
        date_combobox.set("dd")
        category_entry.set("Select Category")
        description_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)

    except Exception as e:
        error_label = tk.Label(tab, text=f"An error occurred: {e}", fg="red")
        error_label.grid(row=5, column=0, columnspan=2, padx=5, pady=2, sticky="w")


def create_add_transaction_tab(tab):
    """Create the 'Add Transaction' tab with income and expense sub-tabs."""
    # Create a frame for the tab titles
    tab_titles_frame = tk.Frame(tab)
    tab_titles_frame.pack(pady=5)  # Use pack to position the frame

    # Create a Notebook for sub-tabs
    sub_notebook = ttk.Notebook(tab)
    sub_notebook.pack(pady=1, expand=True, fill="both")

    # Create Income tab
    tab_income = ttk.Frame(sub_notebook)
    sub_notebook.add(tab_income, text="Income")

    # Create Expense tab
    tab_expense = ttk.Frame(sub_notebook)
    sub_notebook.add(tab_expense, text="Expense")

    # Create forms for income and expense
    create_income_form(tab_income)
    create_expense_form(tab_expense)

    # Optionally select the income tab by default
    sub_notebook.select(tab_income)

def create_income_form(tab):
    """Create the input form for adding income transactions."""
    # Date entry fields
    date_label = tk.Label(tab, text="Date:")
    date_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")

    date_frame = tk.Frame(tab)
    date_frame.grid(row=0, column=1, padx=5, pady=2)

    current_year = date.today().year
    year_values = [str(i) for i in range(current_year - 2, current_year + 3)] 
    year_combobox = ttk.Combobox(date_frame, values=year_values, width=5)
    year_combobox.set("yyyy")
    year_combobox.configure(foreground="#828282")
    year_combobox.pack(side=tk.LEFT)

    month_values = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    month_combobox = ttk.Combobox(date_frame, values=month_values, width=5)
    month_combobox.set("mm")
    month_combobox.configure(foreground="#828282")
    month_combobox.pack(side=tk.LEFT)

    date_values = [str(i).zfill(2) for i in range(1, 32)]
    date_combobox = ttk.Combobox(date_frame, values=date_values, width=5)
    date_combobox.set("dd")
    date_combobox.configure(foreground="#828282")
    date_combobox.pack(side=tk.LEFT)

    # Category entry
    categories = ["Salary", "Stipend", "Freelance", "Other"]
    tk.Label(tab, text="Category:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    category_combobox = ttk.Combobox(tab, values=categories, width=23)
    category_combobox.set("Select Category")
    category_combobox.configure(foreground="#828282")
    category_combobox.grid(row=1, column=1, padx=5, pady=2)

    # Description entry
    tk.Label(tab, text="Description:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    description_entry = tk.Entry(tab, width=26)
    description_entry.grid(row=2, column=1, padx=5, pady=2)

    # Amount entry
    tk.Label(tab, text="Amount:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
    amount_frame = tk.Frame(tab, width=26)
    amount_frame.grid(row=3, column=1, padx=5, pady=2)
    tk.Label(amount_frame, text="$").pack(side=tk.LEFT)
    amount_entry = tk.Entry(amount_frame, width=24)
    amount_entry.pack(side=tk.LEFT)

    # Submit button for adding income
    submit_button = tk.Button(tab, text="Add Income", command=lambda: submit_transaction(date_combobox, month_combobox, year_combobox, category_combobox, description_entry, amount_entry, "income", tab))
    submit_button.grid(row=4, column=0, padx=5, pady=10, sticky="e")  # Aligning the button to the right


def create_expense_form(tab):
    """Create the input form for adding expense transactions."""
    # Date entry fields
    date_label = tk.Label(tab, text="Date:")
    date_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")

    date_frame = tk.Frame(tab)
    date_frame.grid(row=0, column=1, padx=5, pady=2)

    current_year = date.today().year
    year_values = [str(i) for i in range(current_year - 2, current_year + 3)] 
    year_combobox = ttk.Combobox(date_frame, values=year_values, width=5)
    year_combobox.set("yyyy")
    year_combobox.configure(foreground="#828282")
    year_combobox.pack(side=tk.LEFT)

    month_values = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    month_combobox = ttk.Combobox(date_frame, values=month_values, width=5)
    month_combobox.set("mm")
    month_combobox.configure(foreground="#828282")
    month_combobox.pack(side=tk.LEFT)

    date_values = [str(i).zfill(2) for i in range(1, 32)]
    date_combobox = ttk.Combobox(date_frame, values=date_values, width=5)
    date_combobox.set("dd")
    date_combobox.configure(foreground="#828282")
    date_combobox.pack(side=tk.LEFT)

    # Category entry
    categories = ["Food", "Travel", "Utilities", "Repairing", "Bills", "Other"]
    tk.Label(tab, text="Category:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    category_combobox = ttk.Combobox(tab, values=categories, width=23)
    category_combobox.set("Select Category")
    category_combobox.configure(foreground="#828282")
    category_combobox.grid(row=1, column=1, padx=5, pady=2)

    # Description entry
    tk.Label(tab, text="Description:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    description_entry = tk.Entry(tab, width=26)
    description_entry.grid(row=2, column=1, padx=5, pady=2)

    # Amount entry
    tk.Label(tab, text="Amount:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
    amount_frame = tk.Frame(tab, width=26)
    amount_frame.grid(row=3, column=1, padx=5, pady=2)
    tk.Label(amount_frame, text="$").pack(side=tk.LEFT)
    amount_entry = tk.Entry(amount_frame, width=24)
    amount_entry.pack(side=tk.LEFT)

    # Submit button for adding expense
    submit_button = tk.Button(tab, text="Add Expense", command=lambda: submit_transaction(date_combobox, month_combobox, year_combobox, category_combobox, description_entry, amount_entry, "expense", tab))
    submit_button.grid(row=4, column=0, padx=5, pady=10, sticky="e")  # Aligning the button to the right

def show_expenses_by_category(tab):
    """Visualize expenses by category within the tab."""
    # Clear previous visualizations
    for widget in tab.winfo_children():
        widget.destroy()
    
    # Create a frame for the visualization
    viz_frame = tk.Frame(tab)
    viz_frame.pack()

    # Call the function to visualize expenses by category
    visualize_expenses_by_category(viz_frame, db_path)
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

    # Tab 2: Visualize Expenses by Category
    tab_expenses_by_category = ttk.Frame(notebook)
    notebook.add(tab_expenses_by_category, text="Expenses by Category")

    # Tab 3: View All Transactions
    tab_view_all_transactions = ttk.Frame(notebook)
    notebook.add(tab_view_all_transactions, text="View All Transactions")

    # Bind tab change event to handle switching
    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    # Initialize the first tab (Add Transaction)
    create_add_transaction_tab(tab_add_transaction)

    # Start the GUI event loop
    root.mainloop()