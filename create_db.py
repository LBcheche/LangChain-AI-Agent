import sqlite3

# Connect to (or create) the SQLite database
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Create the 'products' table with multiple useful columns
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    price REAL,
    stock INTEGER,
    category TEXT
)
""")

# Insert some sample products into the table
products = [
    ("Mechanical Keyboard", "RGB keyboard with blue switches", 59.99, 20, "Peripherals"),
    ("Gaming Mouse", "High DPI mouse with programmable buttons", 39.99, 35, "Peripherals"),
    ("24-inch Monitor", "Full HD monitor with 75Hz refresh rate", 129.99, 12, "Displays"),
    ("Laptop i5", "Laptop with SSD and 8GB RAM", 749.00, 7, "Computers"),
    ("Gaming Chair", "Reclining chair with ergonomic design", 199.00, 9, "Furniture")
]

# Use executemany to insert all rows in one call
cursor.executemany("""
INSERT INTO products (name, description, price, stock, category)
VALUES (?, ?, ?, ?, ?)
""", products)

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("✅ SQLite database created successfully with 'products' table.")
