# finance_manager.py
from transaction_manager import add_transaction, view_transactions, view_transactions_by_category
from report_generator import generate_report
from db_manager import create_table

def main():
    create_table()  # Ensure the table is created before anything else
    
    while True:
        print("\n--- Personal Finance Manager ---")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. View Transactions by Category")
        print("4. Generate Report")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category (e.g., Food, Rent, Salary): ")
            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            trans_type = input("Enter type (Income/Expense): ")
            
            add_transaction(date, category, description, amount, trans_type)
        
        elif choice == '2':
            view_transactions()
        
        elif choice == '3':
            category = input("Enter category to filter by: ")
            view_transactions_by_category(category)
        
        elif choice == '4':
            generate_report()
        
        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
