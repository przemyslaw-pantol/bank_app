import sqlite3
import random
from datetime import datetime, timedelta

# Database setup
db_name = "banking.db"

# Connect to the database (or create if not exists)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Function to generate random data
def generate_random_transactions(n=10000):
    id_numbers = [f"{random.randint(100000, 999999):012}" for _ in range(5)]  # 5 unique IDs
    types = ["wplata", "wyplata", "przelew"]
    data = []
    
    for _ in range(n):
        id_number = random.choice(id_numbers)
        txn_type = random.choice(types)
        random_date = datetime.now() - timedelta(days=random.randint(0, 30))  # Past 30 days
        date = random_date.strftime("%Y-%m-%d")
        time = random_date.strftime("%H:%M:%S")
        amount = round(random.uniform(1, 500), 2)  # Amount between 1 and 500
        if txn_type == "przelew":
            data.append((id_number, "przelew_wychodzacy",-amount, date, time))
            data.append((random.choice(id_numbers), "przelew_przychodzacy", amount, date, time))
            continue
        if txn_type =="wyplata":
            amount = -amount  # Negative for withdrawals or transfers

        data.append((id_number, txn_type, amount, date, time))
    
    return data

# Insert random data into the database
def insert_random_data(data):
    cursor.executemany("""
    INSERT INTO transactions (id_number, type, amount, date, time)
    VALUES (?, ?, ?, ?, ?)
    """, data)
    conn.commit()

# Generate and insert 20 random transactions
random_data = generate_random_transactions()
insert_random_data(random_data)

# Fetch and display the data to verify
cursor.execute("SELECT * FROM transactions")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the database connection
conn.close()
