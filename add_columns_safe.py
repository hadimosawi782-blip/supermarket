#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اضافه کردن ستون‌های جدید به جدول products بدون حذف دیتا
"""

import sqlite3
import os
import shutil
from datetime import datetime

# مسیر دقیق دیتابیس
DB_PATH = r'C:\Users\RRCC\Desktop\supermarket\supermarket.db'

def backup_database():
    """گرفتن بکاپ خودکار"""
    if os.path.exists(DB_PATH):
        backup_path = f"C:\\Users\\RRCC\\Desktop\\supermarket\\supermarket_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(DB_PATH, backup_path)
        print(f"✅ بکاپ گرفته شد: {backup_path}")
        return True
    return False

def add_columns():
    """اضافه کردن ستون‌های جدید"""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ فایل دیتابیس در مسیر {DB_PATH} وجود ندارد!")
        return False
    
    try:
        # گرفتن بکاپ
        backup_database()
        
        # اتصال به دیتابیس
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # بررسی وجود جدول products
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
        if not cursor.fetchone():
            print("❌ جدول products پیدا نشد!")
            
            # نمایش همه جدول‌ها
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print("\n📋 جدول‌های موجود در دیتابیس:")
            for table in tables:
                print(f"   - {table[0]}")
            return False
        
        # دریافت ستون‌های موجود
        cursor.execute("PRAGMA table_info(products)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"\n📋 ستون‌های موجود در جدول products ({len(columns)} عدد):")
        for col in columns:
            print(f"   - {col}")
        
        added = False
        
        # اضافه کردن ستون is_credit_purchase
        if 'is_credit_purchase' not in columns:
            cursor.execute("ALTER TABLE products ADD COLUMN is_credit_purchase BOOLEAN DEFAULT 0")
            print("\n✅ ستون is_credit_purchase اضافه شد")
            added = True
        else:
            print("\nℹ️ ستون is_credit_purchase قبلاً وجود دارد")
        
        # اضافه کردن ستون credit_amount
        if 'credit_amount' not in columns:
            cursor.execute("ALTER TABLE products ADD COLUMN credit_amount FLOAT DEFAULT 0")
            print("✅ ستون credit_amount اضافه شد")
            added = True
        else:
            print("ℹ️ ستون credit_amount قبلاً وجود دارد")
        
        if added:
            # به‌روزرسانی محصولات قرضی موجود
            cursor.execute("""
                UPDATE products 
                SET is_credit_purchase = 1,
                    credit_amount = (quantity * items_per_carton + single_quantity) * buying_price
                WHERE purchase_type = 'credit' AND creditor_id IS NOT NULL
            """)
            
            updated_count = cursor.rowcount
            print(f"\n📊 {updated_count} محصول قرضی به‌روزرسانی شد")
            
            conn.commit()
            print("\n✅ همه تغییرات با موفقیت اعمال شد")
        else:
            print("\nℹ️ هیچ تغییر جدیدی لازم نبود")
        
        # نمایش آمار نهایی
        cursor.execute("SELECT COUNT(*) FROM products WHERE purchase_type = 'credit'")
        credit_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM products WHERE is_credit_purchase = 1")
        is_credit_count = cursor.fetchone()[0]
        
        print(f"\n📊 آمار نهایی:")
        print(f"   محصولات با purchase_type='credit': {credit_count}")
        print(f"   محصولات با is_credit_purchase=1: {is_credit_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        import traceback
        traceback.print_exc()
        return False

def fix_orphan_credits():
    """رفع قرض‌های یتیم"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("\n" + "=" * 60)
        print("🔧 رفع قرض‌های یتیم")
        print("=" * 60)
        
        # پیدا کردن طلبکارها با قرض اضافی
        cursor.execute("""
            SELECT c.id, c.name, c.current_debt, 
                   COALESCE(SUM((p.quantity * p.items_per_carton + p.single_quantity) * p.buying_price), 0) as real_debt
            FROM creditors c
            LEFT JOIN products p ON p.creditor_id = c.id AND p.purchase_type = 'credit'
            GROUP BY c.id
            HAVING c.current_debt > COALESCE(SUM((p.quantity * p.items_per_carton + p.single_quantity) * p.buying_price), 0) + 1
        """)
        
        fixed = 0
        for creditor in cursor.fetchall():
            creditor_id, name, current_debt, real_debt = creditor
            diff = current_debt - real_debt
            
            print(f"\n📌 طلبکار: {name}")
            print(f"   قرض فعلی: {current_debt:,.0f}")
            print(f"   قرض واقعی: {real_debt:,.0f}")
            print(f"   اختلاف: {diff:,.0f}")
            
            # تصحیح قرض
            cursor.execute("UPDATE creditors SET current_debt = ? WHERE id = ?", (real_debt, creditor_id))
            fixed += 1
            print(f"   ✅ تصحیح شد: {current_debt:,.0f} → {real_debt:,.0f}")
        
        if fixed > 0:
            conn.commit()
            print(f"\n✅ {fixed} طلبکار تصحیح شدند")
        else:
            print("\n✅ هیچ قرض اضافی یافت نشد")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ خطا در رفع قرض: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🛠️ ابزار اضافه کردن ستون‌های قرض به جدول products")
    print("=" * 60)
    print(f"📁 مسیر دیتابیس: {DB_PATH}")
    print()
    
    # اضافه کردن ستون‌ها
    if add_columns():
        print("\n" + "=" * 60)
        print("✅ عملیات با موفقیت انجام شد")
        print("=" * 60)
        
        # رفع قرض‌های اضافی
        fix_orphan_credits()
        
        print("\n" + "=" * 60)
        print("🔧 حالا می‌توانید تابع delete_product را در routes.py اصلاح کنید")
        print("=" * 60)
    else:
        print("\n❌ عملیات با خطا مواجه شد")