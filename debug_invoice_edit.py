#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اسکریپت دیباگ برای مشکل ویرایش فاکتور فروش
"""

import sys
import os
import traceback

# افزودن مسیر پروژه
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app, db
    from app.models import Sale, SaleItem, Customer, Product
    from flask import url_for
    from werkzeug.routing import BuildError
    
    app = create_app()
    app.app_context().push()
    
    print("=" * 80)
    print("🔍 شروع فرآیند دیباگ ویرایش فاکتور فروش")
    print("=" * 80)
    
    # 1. بررسی وجود مسیر (route) ویرایش فاکتور
    print("\n📌 1. بررسی مسیرهای مربوط به ویرایش فاکتور:")
    print("-" * 40)
    
    routes_to_check = [
        'main_bp.edit_sale',
        'main_bp.edit_invoice', 
        'sale_bp.edit_sale',
        'sales.edit_sale',
        'main_bp.sale_edit'
    ]
    
    found_routes = []
    for route in routes_to_check:
        try:
            url = url_for(route, sale_id=1)
            print(f"✅ مسیر '{route}' وجود دارد: {url}")
            found_routes.append(route)
        except BuildError as e:
            print(f"❌ مسیر '{route}' وجود ندارد")
        except Exception as e:
            print(f"⚠️ خطا در بررسی '{route}': {str(e)}")
    
    # 2. بررسی تمام مسیرهای ثبت شده
    print("\n📌 2. لیست تمام مسیرهای موجود در برنامه:")
    print("-" * 40)
    all_routes = []
    for rule in app.url_map.iter_rules():
        if 'edit' in rule.rule or 'sale' in rule.rule:
            all_routes.append(f"{rule.endpoint}: {rule.rule}")
            print(f"   • {rule.endpoint}: {rule.rule}")
    
    if not found_routes:
        print("\n⚠️ هیچ مسیر ویرایش فاکتوری پیدا نشد!")
        print("مسیرهای موجود با کلمه 'edit' یا 'sale':")
        for r in all_routes[:10]:
            print(f"   {r}")
    
    # 3. بررسی مدل Sale و فیلدهای آن
    print("\n📌 3. بررسی مدل Sale (فاکتور فروش):")
    print("-" * 40)
    try:
        # بررسی وجود جدول
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'sale' in tables:
            print("✅ جدول 'sale' وجود دارد")
            columns = inspector.get_columns('sale')
            print(f"   تعداد فیلدها: {len(columns)}")
            print("   فیلدهای اصلی:")
            for col in columns[:10]:
                print(f"     - {col['name']}: {col['type']}")
        else:
            print("❌ جدول 'sale' وجود ندارد!")
            
    except Exception as e:
        print(f"❌ خطا در بررسی جدول: {str(e)}")
    
    # 4. بررسی وجود یک فاکتور نمونه
    print("\n📌 4. بررسی فاکتورهای موجود:")
    print("-" * 40)
    try:
        sales = Sale.query.limit(5).all()
        if sales:
            print(f"✅ تعداد فاکتورهای موجود: {Sale.query.count()}")
            for sale in sales:
                print(f"   • ID: {sale.id}, مشتری: {sale.customer_name}, تاریخ: {sale.date}, مبلغ: {sale.total_amount}")
        else:
            print("⚠️ هیچ فاکتوری در دیتابیس وجود ندارد!")
    except Exception as e:
        print(f"❌ خطا در خواندن فاکتورها: {str(e)}")
    
    # 5. بررسی وجود قالب (template) ویرایش
    print("\n📌 5. بررسی قالب‌های ویرایش:")
    print("-" * 40)
    template_paths = [
        'app/templates/edit_sale.html',
        'app/templates/sales/edit_sale.html',
        'app/templates/invoice_edit.html',
        'app/templates/edit_invoice.html'
    ]
    
    for template_path in template_paths:
        if os.path.exists(template_path):
            print(f"✅ قالب وجود دارد: {template_path}")
        else:
            print(f"❌ قالب وجود ندارد: {template_path}")
    
    # 6. بررسی کد مربوط به ویرایش در routes.py
    print("\n📌 6. بررسی فایل routes.py:")
    print("-" * 40)
    routes_file = 'app/routes.py'
    if os.path.exists(routes_file):
        with open(routes_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # جستجوی توابع ویرایش
        import re
        edit_functions = re.findall(r'def\s+(\w*edit\w*_\w*|\w*edit\w*)\s*\([^)]*\):', content, re.IGNORECASE)
        if edit_functions:
            print("✅ توابع ویرایش پیدا شده در routes.py:")
            for func in set(edit_functions):
                print(f"   • {func}")
        else:
            print("⚠️ هیچ تابع ویرایشی در routes.py پیدا نشد!")
            
        # جستجوی مسیرهای edit
        edit_routes = re.findall(r"@main_bp\.route\('[^']*edit[^']*'[^)]*\)", content, re.IGNORECASE)
        if edit_routes:
            print("\n✅ مسیرهای ویرایش در routes.py:")
            for route in edit_routes[:5]:
                print(f"   • {route}")
    else:
        print("❌ فایل routes.py پیدا نشد!")
    
    # 7. بررسی خطاهای احتمالی در دکمه ویرایش
    print("\n📌 7. بررسی ساختار دکمه ویرایش در قالب:")
    print("-" * 40)
    template_file = 'app/templates/sales.html'
    if os.path.exists(template_file):
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # جستجوی لینک‌های ویرایش
        edit_links = re.findall(r'url_for\([^)]*edit[^)]*\)', content, re.IGNORECASE)
        if edit_links:
            print("✅ لینک‌های ویرایش پیدا شده در sales.html:")
            for link in edit_links[:3]:
                print(f"   • {link}")
        else:
            print("⚠️ هیچ لینک ویرایشی در sales.html پیدا نشد!")
            
        # جستجوی دکمه‌های ویرایش
        edit_buttons = re.findall(r'<a[^>]*edit[^>]*>.*?</a>', content, re.IGNORECASE | re.DOTALL)
        if edit_buttons:
            print(f"\n✅ {len(edit_buttons)} دکمه ویرایش پیدا شد:")
            for btn in edit_buttons[:2]:
                print(f"   • {btn[:150]}...")
    else:
        print("❌ فایل sales.html پیدا نشد!")
    
    # 8. تست اتصال به دیتابیس
    print("\n📌 8. تست اتصال دیتابیس:")
    print("-" * 40)
    try:
        from sqlalchemy import text
        result = db.session.execute(text("SELECT 1"))
        print("✅ اتصال دیتابیس برقرار است")
    except Exception as e:
        print(f"❌ خطا در اتصال دیتابیس: {str(e)}")
    
    # 9. جمع‌بندی و راهنمایی
    print("\n" + "=" * 80)
    print("📋 جمع‌بندی و راهنمایی:")
    print("=" * 80)
    
    if not found_routes:
        print("\n❌ مشکل اصلی: مسیر ویرایش فاکتور تعریف نشده است!")
        print("\n🔧 راه حل: به فایل routes.py اضافه کنید:")
        print("""
@main_bp.route('/edit_sale/<int:sale_id>', methods=['GET', 'POST'])
@login_required
def edit_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    if request.method == 'POST':
        # منطق ویرایش
        sale.customer_name = request.form['customer_name']
        sale.total_amount = float(request.form['total_amount'])
        db.session.commit()
        flash('فاکتور با موفقیت ویرایش شد', 'success')
        return redirect(url_for('main_bp.sales_list'))
    return render_template('edit_sale.html', sale=sale)
        """)
    
    print("\n✅ اسکریپت دیباگ کامل شد!")
    print("=" * 80)
    
except Exception as e:
    print(f"\n❌ خطای غیرمنتظره: {str(e)}")
    print(traceback.format_exc())