import sqlite3

# Connect to SQLite DB (creates file if not exists)
conn = sqlite3.connect("data/business.db")
cursor = conn.cursor()

# Drop tables if they already exist (for re-runs)
cursor.execute("DROP TABLE IF EXISTS sales")
cursor.execute("DROP TABLE IF EXISTS customers")
cursor.execute("DROP TABLE IF EXISTS inventory")

# Create tables
cursor.execute('''
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    join_date DATE
)
''')

cursor.execute('''
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    category TEXT,
    price REAL,
    stock INTEGER
)
''')

cursor.execute('''
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    sale_date DATE,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(product_id) REFERENCES inventory(id)
)
''')

# Insert mock customers
customers = [
    ('Alice Johnson', 'alice@example.com', '2023-01-10'),
    ('Bob Smith', 'bob@example.com', '2023-03-12'),
    ('Charlie Lee', 'charlie@example.com', '2023-06-05')
]
cursor.executemany('INSERT INTO customers (name, email, join_date) VALUES (?, ?, ?)', customers)

# Insert mock products
products = [
    ('Laptop', 'Electronics', 1200.0, 20),
    ('Headphones', 'Electronics', 150.0, 50),
    ('Desk Chair', 'Furniture', 250.0, 30)
]
cursor.executemany('INSERT INTO inventory (product_name, category, price, stock) VALUES (?, ?, ?, ?)', products)

# Insert mock sales
sales = [
    (1, 1, 1, '2024-03-10'),
    (2, 2, 1, '2024-03-15'),
    (1, 2, 2, '2024-04-01'),
    (3, 3, 1, '2024-04-07')
]
cursor.executemany('INSERT INTO sales (customer_id, product_id, quantity, sale_date) VALUES (?, ?, ?, ?)', sales)

# Commit and close
conn.commit()
conn.close()

print("✅ Mock business database created successfully.")
