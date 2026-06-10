import sqlite3
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# حذف دیتابیس قدیمی اگر وجود دارد
db_path = 'instance/app.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print("✅ دیتابیس قدیمی حذف شد")

# ایجاد دیتابیس جدید
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. ایجاد جدول license
cursor.execute('''
CREATE TABLE license (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hw_id VARCHAR(128) NOT NULL,
    expire_at DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    trial_count INTEGER DEFAULT 0,
    last_trial_date DATETIME,
    license_type VARCHAR(20) DEFAULT 'trial',
    last_valid_date DATETIME
)
''')
print("✅ جدول license ایجاد شد")

# 2. ایجاد جدول users
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) DEFAULT 'مدیر',
    role VARCHAR(20) DEFAULT 'manager',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ جدول users ایجاد شد")

# 3. ایجاد جدول alembic_version (برای flask-migrate)
cursor.execute('''
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL
)
''')
cursor.execute("INSERT INTO alembic_version (version_num) VALUES ('head')")
print("✅ جدول alembic_version ایجاد شد")

# 4. اضافه کردن کاربر ادمین
hashed_password = generate_password_hash('admin123')
cursor.execute('''
INSERT INTO users (username, password_hash, full_name, role)
VALUES (?, ?, ?, ?)
''', ('admin', hashed_password, 'مدیر سیستم', 'admin'))
print("✅ کاربر ادمین ایجاد شد (admin / admin123)")

# 5. اضافه کردن یک رکورد license معتبر
expire_date = datetime.now() + timedelta(days=365)
cursor.execute('''
INSERT INTO license (hw_id, expire_at, created_at, trial_count, license_type, last_valid_date)
VALUES (?, ?, ?, ?, ?, ?)
''', ('test_hardware_id', expire_date, datetime.now(), 0, 'full', datetime.now()))
print("✅ رکورد license ایجاد شد")

conn.commit()

# نمایش لیست جداول برای تایید
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("\n📋 لیست جداول ایجاد شده:")
for table in tables:
    print(f"   - {table[0]}")

conn.close()
print("\n✅ دیتابیس با موفقیت بازسازی شد")
input("برای خروج Enter را بزنید...")