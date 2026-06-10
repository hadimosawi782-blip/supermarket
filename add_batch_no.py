# add_batch_no.py
import sqlite3
import os

def add_batch_no_column():
    """اضافه کردن ستون batch_no به جدول products"""
    db_path = 'supermarket.db'
    
    if not os.path.exists(db_path):
        print(f"❌ فایل دیتابیس {db_path} وجود ندارد")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # بررسی وجود ستون batch_no
        cursor.execute("PRAGMA table_info(products)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'batch_no' not in columns:
            print("➕ اضافه کردن ستون batch_no...")
            cursor.execute("ALTER TABLE products ADD COLUMN batch_no VARCHAR(50)")
            print("✅ ستون batch_no اضافه شد")
        else:
            print("✅ ستون batch_no از قبل وجود دارد")
        
        # بررسی وجود ستون‌های دیگر اگر لازم است
        required_columns = ['expiry_date', 'purchase_type', 'creditor_id', 'purchase_description']
        for col in required_columns:
            if col not in columns:
                print(f"⚠️ ستون {col} وجود ندارد")
        
        conn.commit()
        print("\n🎉 عملیات با موفقیت انجام شد")
        return True
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()

if __name__ == "__main__":
    add_batch_no_column()