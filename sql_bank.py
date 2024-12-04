import sqlite3
import random
from datetime import datetime
import pandas as pd
import wx

def client_nr(id):
    padded_id = f"{id:06}"  # Zero-pad the ID to 6 digits
    random_digits = ''.join(str(random.randint(0, 9)) for _ in range(6))  # Generate 6 random digits
    return f"{padded_id}{random_digits}"

def add_client(name, surname, db):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT MAX(id) + 1 FROM customers")
            result = cursor.fetchone()
            new_id = result[0] if result[0] is not None else 1  # Default to 1 if table is empty
            
            # Generate client number
            id_number = client_nr(new_id)
            
            # Insert the new client
            cursor.execute("""
            INSERT INTO customers (name, surname, id_number)
            VALUES (?, ?, ?)
            """,(name, surname, id_number))
            conn.commit()
            return id_number  
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def find_client_id(id, conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM customers WHERE id_number = ?
        """, (id,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def transaction_log(id_number, type, amount, conn):
    try:
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        date = now.date()
        
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO transactions (id_number, type, amount, date, time)
        VALUES (?, ?, ?, ?, ?)
        """, (id_number, type, amount, date, time))
        conn.commit() 
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def client_info(name, surname, conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM customers WHERE name = ? AND surname = ?
        """, (name, surname))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def update_balance(id, amount, db, mark):
    try:
        amount = float(amount)
        with sqlite3.connect(db) as conn:
            client = find_client_id(id, conn)
            if not client:
                raise ValueError('Client not found')
            elif float(amount) < 0:
                raise ValueError('Invalid amount')

            # Initialize new balance
            new_balance = float(client[3])  # Current balance
            
            match mark:
                case "+":
                    new_balance += amount
                    transaction_log(id, "deposit", amount, conn)
                case "-":
                    if new_balance < amount:
                        raise ValueError('Insufficient funds')
                    new_balance -= amount
                    transaction_log(id, "withdrawal", -amount, conn)
                case _:
                    print("Invalid mark")
                    return  # Exit function for invalid mark

            # Update balance in the database
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE customers SET balance = ? WHERE id_number = ?
            """, (new_balance, id))
            
            conn.commit()
            return new_balance  # Return updated balance for confirmation

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except ValueError as e:
        print(f"Value error: {e}")

def find_log(id,db):

    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            data=cursor.execute("""
            SELECT * FROM transactions WHERE id_number = ? 
            """, (id,))
            return data
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    
def date_stats(start, end, db):
    start=start.Format('%Y-%m-%d') 
    end=end.Format('%Y-%m-%d')

    try:
        with sqlite3.connect(db) as conn:
            query = """
            SELECT * FROM transactions WHERE date BETWEEN ? AND ?
            """
            df = pd.read_sql_query(query, conn, params=(start, end))
        
        print(df)  
        return df  
    
    except Exception as e:
        print(f"An error occurred: {e}")  
