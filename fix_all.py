# fix_all.py
from app import create_app, db

app = create_app()

with app.app_context():
    print("📦 در حال تعمیر دیتابیس...")
    
    # ۱. ساخت foreign_products
    try:
        db.session.execute("""
            CREATE TABLE foreign_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                batch_no VARCHAR(50) NOT NULL,
                buying_price FLOAT NOT NULL DEFAULT 0,
                selling_price FLOAT NOT NULL DEFAULT 0,
                unit VARCHAR(20) DEFAULT 'عدد',
                description TEXT,
                profit_per_item FLOAT DEFAULT 0,
                added_by INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ جدول foreign_products ساخته شد")
    except Exception as e:
        print(f"⚠️ foreign_products: {e}")
    
    # ۲. اضافه کردن foreign_product_id به sale_items
    try:
        db.session.execute("ALTER TABLE sale_items ADD COLUMN foreign_product_id INTEGER")
        print("✅ ستون foreign_product_id اضافه شد")
    except Exception as e:
        print(f"⚠️ foreign_product_id: {e}")
    
    # ۳. ساخت foreign_products اگر با خطای قبلی ساخته نشد
    try:
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS foreign_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                batch_no VARCHAR(50) NOT NULL,
                buying_price FLOAT NOT NULL DEFAULT 0,
                selling_price FLOAT NOT NULL DEFAULT 0,
                unit VARCHAR(20) DEFAULT 'عدد',
                description TEXT,
                profit_per_item FLOAT DEFAULT 0,
                added_by INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ جدول foreign_products تأیید شد")
    except Exception as e:
        print(f"⚠️ {e}")
    
    db.session.commit()
    print("🎉 دیتابیس آماده است!")
    print("🔥 حالا می‌توانی برنامه را اجرا کنی")