import sqlite3
import pandas as pd

DB_NAME = 'finance.db'

def create_connection():
    """ Create a database connection to the SQLite database """
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_transaction_table(db_path):
    """ Create the transactions table if it doesn't exist """
    conn = sqlite3.connect(db_path)  # Use the db_path parameter
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            description TEXT,
            amount REAL,
            type TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(date, category, description, amount, trans_type):
    """ Insert a new transaction into the transactions table """
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO transactions (date, category, description, amount, type)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, category, description, amount, trans_type))
    
    conn.commit()
    conn.close()

def fetch_transactions():
    """ Fetch all transactions from the transactions table """
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM transactions')
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def fetch_transactions_by_category(category):
    """ Fetch transactions by category """
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM transactions WHERE category = ?', (category,))
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def get_all_transactions(db_path):
    """Fetch all transactions from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")  # Adjust the query based on your table structure
    transactions = cursor.fetchall()
    conn.close()
    return [f"Type: {t[5]}, Amount: ${t[4]:.2f}, Category: {t[2]}" for t in transactions]  # Adjust indexes based on your schema


def get_filtered_data(db_path, year, month):
    """Retrieve filtered data based on year and month from the database."""
    conn = sqlite3.connect(db_path)
    query = """
    SELECT category,
           SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS Income,
           SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS Expenses
    FROM transactions  -- Make sure the table name matches (case-sensitive)
    WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
    GROUP BY category
    """

    # Execute the query with parameters
    filtered_data = pd.read_sql_query(query, conn, params=(year, month))
    conn.close()

    return filtered_data