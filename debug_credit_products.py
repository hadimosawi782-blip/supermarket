#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اسکریپت جامع دیباگ برای بررسی مشکل قرض محصولات
مشکل: افزایش قرض هنگام ثبت محصول قرضی، اما کاهش نیافتن هنگام حذف
"""

import sys
import os
from datetime import datetime

# اضافه کردن مسیر پروژه
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Product, Creditor, DebtTransaction

app = create_app()
app.app_context().push()

def print_section(title):
    """چاپ بخش با خط کشی"""
    print("\n" + "=" * 80)
    print(f"📌 {title}")
    print("=" * 80)

def print_subsection(title):
    """چاپ زیربخش"""
    print(f"\n🔹 {title}")
    print("-" * 50)

def check_product_model():
    """بررسی مدل Product و فیلدهای مربوط به قرض"""
    print_section("1. بررسی مدل Product (فیلدهای مربوط به قرض)")
    
    # لیست فیلدهای مدل Product
    product_columns = [c.name for c in Product.__table__.columns]
    
    print("\n📋 فیلدهای موجود در مدل Product:")
    for col in product_columns:
        print(f"   - {col}")
    
    # بررسی فیلدهای کلیدی
    credit_related_fields = ['purchase_type', 'creditor_id', 'is_credit_purchase', 'credit_amount']
    print("\n🎯 فیلدهای مربوط به خرید قرضی:")
    for field in credit_related_fields:
        if field in product_columns:
            print(f"   ✅ {field}: وجود دارد")
        else:
            print(f"   ❌ {field}: وجود ندارد (مشکل احتمالی!)")

def check_creditor_model():
    """بررسی مدل Creditor"""
    print_section("2. بررسی مدل Creditor")
    
    creditor_columns = [c.name for c in Creditor.__table__.columns]
    
    print("\n📋 فیلدهای موجود در مدل Creditor:")
    for col in creditor_columns:
        print(f"   - {col}")
    
    # بررسی فیلد current_debt
    if 'current_debt' in creditor_columns:
        print("\n✅ فیلد current_debt وجود دارد")
    else:
        print("\n❌ فیلد current_debt وجود ندارد (مشکل بزرگ!)")

def check_credit_products():
    """بررسی محصولات قرضی موجود"""
    print_section("3. بررسی محصولات قرضی موجود در سیستم")
    
    # محصولات با purchase_type = credit
    credit_products = Product.query.filter(Product.purchase_type == "credit").all()
    
    print(f"\n📦 تعداد کل محصولات قرضی: {len(credit_products)}")
    
    if not credit_products:
        print("   ⚠️ هیچ محصول قرضی در سیستم وجود ندارد!")
        return
    
    total_expected_credit = 0
    
    for i, p in enumerate(credit_products, 1):
        creditor_name = p.creditor.name if p.creditor else "❌ بدون طلبکار"
        total_qty = p.total_items
        expected_credit = total_qty * (p.buying_price or 0)
        total_expected_credit += expected_credit
        
        print(f"\n   {i}. 🏷️ {p.name} (ID: {p.id})")
        print(f"      طلبکار: {creditor_name}")
        print(f"      نوع خرید: {p.purchase_type}")
        print(f"      تعداد کل: {total_qty} عدد")
        print(f"      قیمت خرید: {p.buying_price:,.0f} افغانی")
        print(f"      قرض مورد انتظار: {expected_credit:,.0f} افغانی")
        
        # بررسی فیلدهای اضافی اگر وجود دارند
        if hasattr(p, 'is_credit_purchase'):
            print(f"      is_credit_purchase: {p.is_credit_purchase}")
        if hasattr(p, 'credit_amount'):
            print(f"      credit_amount: {p.credit_amount:,.0f} افغانی")
            if p.credit_amount != expected_credit:
                print(f"      ⚠️ اختلاف در credit_amount!")
    
    print(f"\n📊 جمع کل قرض مورد انتظار از محصولات: {total_expected_credit:,.0f} افغانی")

def check_creditors_debt():
    """بررسی وضعیت قرض طلبکارها"""
    print_section("4. بررسی وضعیت قرض طلبکارها")
    
    creditors = Creditor.query.all()
    
    if not creditors:
        print("⚠️ هیچ طلبکاری در سیستم وجود ندارد!")
        return
    
    print(f"\n🏢 تعداد کل طلبکارها: {len(creditors)}")
    
    total_system_debt = 0
    total_real_debt = 0
    
    for c in creditors:
        # محاسبه قرض واقعی از محصولات قرضی این طلبکار
        real_debt = 0
        for p in c.products:
            if p.purchase_type == "credit":
                real_debt += p.total_items * (p.buying_price or 0)
        
        system_debt = c.current_debt or 0
        difference = system_debt - real_debt
        
        total_system_debt += system_debt
        total_real_debt += real_debt
        
        print(f"\n   🏢 {c.name} (ID: {c.id})")
        print(f"      قرض ثبت شده در سیستم: {system_debt:,.0f} افغانی")
        print(f"      قرض واقعی از محصولات: {real_debt:,.0f} افغانی")
        print(f"      اختلاف: {difference:+,.0f} افغانی")
        
        if difference > 0:
            print(f"      🔴 مشکل: {difference:,.0f} افغانی قرض اضافی وجود دارد!")
        elif difference < 0:
            print(f"      🟡 توجه: {abs(difference):,.0f} افغانی قرض کمتر از حد انتظار است!")
        else:
            print(f"      ✅ درست است")
    
    print(f"\n📊 جمع کل قرض در سیستم: {total_system_debt:,.0f} افغانی")
    print(f"📊 جمع کل قرض واقعی: {total_real_debt:,.0f} افغانی")
    print(f"📊 اختلاف کلی: {total_system_debt - total_real_debt:+,.0f} افغانی")

def check_debt_transactions():
    """بررسی تاریخچه تراکنش‌های قرض"""
    print_section("5. بررسی تاریخچه تراکنش‌های قرض")
    
    transactions = DebtTransaction.query.order_by(DebtTransaction.date_created.desc()).limit(20).all()
    
    if not transactions:
        print("⚠️ هیچ تراکنش قرضی ثبت نشده است!")
        return
    
    print(f"\n📋 آخرین {len(transactions)} تراکنش قرض:")
    
    for t in transactions:
        creditor_name = t.creditor.name if t.creditor else "نامشخص"
        user_name = t.user.full_name if t.user else "سیستم"
        
        print(f"\n   🧾 {t.transaction_type}")
        print(f"      طلبکار: {creditor_name}")
        print(f"      مبلغ: {t.amount:+,.0f} افغانی")
        print(f"      تاریخ: {t.date_created.strftime('%Y-%m-%d %H:%M') if t.date_created else 'نامشخص'}")
        print(f"      ثبت کننده: {user_name}")
        print(f"      توضیحات: {t.description or '---'}")

def check_delete_function():
    """بررسی وجود تابع حذف و منطق آن"""
    print_section("6. بررسی تابع حذف محصول")
    
    # بررسی فایل routes.py
    routes_file = 'app/routes.py'
    if os.path.exists(routes_file):
        with open(routes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # جستجوی تابع حذف محصول
        import re
        delete_patterns = [
            r'@main_bp\.route\([^)]*delete[^)]*\)\s*def\s+delete_product',
            r'@main_bp\.route\([^)]*delete[^)]*\)\s*def\s+product_delete',
            r'def\s+delete_product\s*\(',
            r'def\s+product_delete\s*\(',
        ]
        
        found = False
        for pattern in delete_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found = True
                print(f"✅ تابع حذف محصول پیدا شد")
                
                # استخراج محتوای تابع
                match = re.search(r'(def\s+delete_product\s*\([^:]*:.*?)(?=\n@|\ndef\s|\Z)', content, re.DOTALL | re.IGNORECASE)
                if match:
                    print("\n📝 محتوای تابع حذف محصول:")
                    print("-" * 40)
                    print(match.group(1)[:1000])  # نمایش 1000 کاراکتر اول
                    print("-" * 40)
                break
        
        if not found:
            print("❌ تابع حذف محصول پیدا نشد!")
            print("   این مشکل اصلی است - سیستم تابع حذف ندارد یا نام آن متفاوت است")
            
            # جستجوی هر تابع delete ای
            all_deletes = re.findall(r'def\s+(\w*delete\w*)\s*\(', content, re.IGNORECASE)
            if all_deletes:
                print(f"\n   توابع حذف موجود: {', '.join(all_deletes)}")
    else:
        print("❌ فایل routes.py پیدا نشد!")

def check_add_function():
    """بررسی تابع ثبت محصول از نظر به‌روزرسانی قرض"""
    print_section("7. بررسی تابع ثبت محصول")
    
    routes_file = 'app/routes.py'
    if os.path.exists(routes_file):
        with open(routes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # جستجوی توابع ثبت محصول
        import re
        add_patterns = [
            r'def\s+add_product\s*\(',
            r'def\s+product_add\s*\(',
            r'def\s+add_credit_product\s*\(',
        ]
        
        for pattern in add_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                print(f"✅ تابع ثبت محصول پیدا شد: {pattern}")
                
                # استخراج محتوای تابع
                match = re.search(r'(' + pattern + r'.*?)(?=\n@|\ndef\s|\Z)', content, re.DOTALL | re.IGNORECASE)
                if match:
                    func_content = match.group(1)[:1500]
                    
                    # بررسی وجود به‌روزرسانی قرض
                    if 'creditor' in func_content.lower() and ('debt' in func_content.lower() or 'current_debt' in func_content.lower()):
                        print("   ✅ به نظر می‌رسد قرض در تابع ثبت به‌روز می‌شود")
                    else:
                        print("   ⚠️ ممکن است قرض در تابع ثبت به‌روز نشود!")
                break

def run_full_debug():
    """اجرای همه بررسی‌ها"""
    print("\n" + "🔍" * 40)
    print("شروع دیباگ جامع سیستم قرض محصولات")
    print("🔍" * 40)
    
    check_product_model()
    check_creditor_model()
    check_credit_products()
    check_creditors_debt()
    check_debt_transactions()
    check_delete_function()
    check_add_function()
    
    print_section("8. جمع‌بندی و راهکارهای پیشنهادی")
    
    print("""
📋 بر اساس اطلاعات بالا:

🔴 مشکلات احتمالی:
   1. فیلدهای is_credit_purchase و credit_amount در مدل Product وجود ندارند
   2. تابع حذف محصول (delete_product) وجود ندارد یا قرض را کاهش نمی‌دهد
   3. در تابع حذف، قرض طلبکار به‌روز نمی‌شود
   4. تراکنش کاهش قرض ثبت نمی‌شود

✅ راهکارهای پیشنهادی:
   1. اضافه کردن فیلدهای is_credit_purchase و credit_amount به مدل Product
   2. ایجاد یا اصلاح تابع delete_product با منطق کاهش قرض
   3. در تابع delete_product:
      - محاسبه مبلغ قرض محصول (تعداد × قیمت خرید)
      - کاهش current_debt طلبکار
      - ثبت تراکنش DebtTransaction با مقدار منفی
   4. اطمینان از اینکه در تابع add_product قرض به درستی افزایش می‌یابد

🛠️ برای رفع مشکل فوری، اسکریپت زیر را اجرا کنید:
   python fix_orphan_credits.py
""")

if __name__ == "__main__":
    try:
        run_full_debug()
    except Exception as e:
        print(f"\n❌ خطا در اجرای دیباگ: {str(e)}")
        import traceback
        traceback.print_exc()