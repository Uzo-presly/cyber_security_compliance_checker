# 2. Dummy SQLite CRM Example
# ---------------------------
# A very basic CRM system that stores customer PII securely.
# Note: In real applications, you'd want to hash or encrypt PII where needed.

import sqlite3

# Connect to SQLite DB (or create one)
conn = sqlite3.connect("crm.db")
cursor = conn.cursor()

# Create a customers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    consent BOOLEAN DEFAULT 0
)
''')

# Insert dummy customer data
cursor.execute("INSERT INTO customers (name, email, phone, consent) VALUES (?, ?, ?, ?)",
               ("Jane Doe", "jane@example.com", "555-0101", True))

conn.commit()
print("Customer data added.")

# Retrieve and display data
for row in cursor.execute("SELECT * FROM customers"):
    print(row)

conn.close()
