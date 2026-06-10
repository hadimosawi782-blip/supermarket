import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("supermarket.db")
cursor = conn.cursor()

print("⚠️ Deleting all old users...")
cursor.execute("DELETE FROM users")

users = [
    ("admin", "1234", "مدیر سیستم", "admin"),
    ("cashier", "1234", "صندوقدار", "cashier"),
    ("manager", "1234", "مدیر فروشگاه", "manager"),
    ("seller", "1234", "فروشنده", "seller")
]

for username, password, fullname, role in users:
    hashed = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
        (username, hashed, fullname, role)
    )

conn.commit()
conn.close()

print("✅ New users created successfully!")
