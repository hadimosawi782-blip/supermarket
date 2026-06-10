# fix_inventory.py
import sys
import os

# اضافه کردن مسیر پروژه
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Product

def fix_inventory():
    """اصلاح موجودی منفی و نامتناسب محصولات"""
    
    app = create_app()
    with app.app_context():
        print("=" * 60)
        print("🔧 شروع اصلاح موجودی محصولات")
        print("=" * 60)
        
        products = Product.query.all()
        
        if not products:
            print("❌ هیچ محصولی در دیتابیس یافت نشد")
            return
        
        fixed_count = 0
        for product in products:
            items_per_carton = product.items_per_carton or 1
            
            # محاسبه موجودی صحیح به صورت دانه
            total_items = (product.quantity * items_per_carton) + product.single_quantity
            
            old_cartons = product.quantity
            old_singles = product.single_quantity
            
            # اگر موجودی منفی است
            if total_items < 0:
                product.quantity = 0
                product.single_quantity = 0
                fixed_count += 1
                print(f"⚠️ {product.name}: موجودی منفی {total_items} به صفر اصلاح شد")
                print(f"   قبل: کارتن={old_cartons}, تک={old_singles}")
                print(f"   بعد: کارتن=0, تک=0")
            
            # اگر موجودی مثبت است اما کارتن و تک نامتناسب است
            elif total_items >= 0:
                new_cartons = total_items // items_per_carton
                new_singles = total_items % items_per_carton
                
                if product.quantity != new_cartons or product.single_quantity != new_singles:
                    product.quantity = new_cartons
                    product.single_quantity = new_singles
                    fixed_count += 1
                    print(f"📦 {product.name}: اصلاح موجودی")
                    print(f"   قبل: کارتن={old_cartons}, تک={old_singles}, کل={total_items}")
                    print(f"   بعد: کارتن={new_cartons}, تک={new_singles}, کل={total_items}")
        
        db.session.commit()
        
        print("=" * 60)
        print(f"✅ اصلاح موجودی انجام شد! {fixed_count} محصول تصحیح شدند.")
        print("=" * 60)

def show_inventory():
    """نمایش موجودی فعلی محصولات"""
    app = create_app()
    with app.app_context():
        print("\n" + "=" * 60)
        print("📊 موجودی فعلی محصولات")
        print("=" * 60)
        
        products = Product.query.all()
        
        if not products:
            print("❌ هیچ محصولی یافت نشد")
            return
        
        for product in products:
            items_per_carton = product.items_per_carton or 1
            total_items = (product.quantity * items_per_carton) + product.single_quantity
            
            print(f"\n📦 {product.name}")
            print(f"   کارتن: {product.quantity}")
            print(f"   تعداد در کارتن: {items_per_carton}")
            print(f"   تک: {product.single_quantity}")
            print(f"   مجموع دانه: {total_items}")
        
        print("=" * 60)

if __name__ == "__main__":
    print("1. نمایش موجودی فعلی")
    print("2. اصلاح موجودی منفی")
    print("3. انجام هر دو")
    
    choice = input("\nانتخاب کنید (1/2/3): ").strip()
    
    if choice == "1":
        show_inventory()
    elif choice == "2":
        fix_inventory()
    elif choice == "3":
        show_inventory()
        print("\n" + "=" * 60)
        fix_inventory()
        print("\n" + "=" * 60)
        show_inventory()
    else:
        print("❌ انتخاب نامعتبر! اجرای اصلاح موجودی...")
        fix_inventory()
    
    input("\nبرای خروج Enter را بزنید...")