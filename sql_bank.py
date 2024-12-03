import sqlite3
import random
 
def create_tables():
    conn = sqlite3.connect("banking.db")
    cursor = conn.cursor()

    # Create customers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id_number TEXT NOT NULL,
        type TEXT NOT NULL,
        amount REAL DEFAULT 0.0,
        date DATE,
        time TIME
    )
    """)
    conn.commit()
    conn.close()

create_tables()

def client_nr(id):
    padded_id = f"{id:06}"  # Zero-pad the ID to 6 digits
    random_digits = ''.join(str(random.randint(0, 9)) for _ in range(6))  # Generate 6 random digits
    return f"{padded_id}{random_digits}"

def add_client(name, surname, db):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT MAX(id) + 1 FROM customers")
        result = cursor.fetchone()
        new_id = result[0] if result[0] is not None else 1  # Default to 1 if table is empty
        print(new_id)
        # Generate client number
        id_number = client_nr(new_id)
        print(id_number)
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
    
    finally:
        conn.close()