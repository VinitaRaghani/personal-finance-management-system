# transaction_manager.py

from db_manager import insert_transaction

def add_transaction(date, category, description, amount, trans_type):
    """ Add a transaction by calling the db_manager """
    try:
        insert_transaction(date, category, description, amount, trans_type)
    except Exception as e:
        raise e
