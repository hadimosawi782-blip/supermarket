# فایل reset_db.py - فقط کاربران
from app import create_app, db
from app.models import *
from datetime import datetime

app = create_app()

with app.app_context():
    print("🧹 در حال پاکسازی دیتابیس...")
    db.drop_all()
    print("🔧 در حال ایجاد جداول جدید...")
    db.create_all()
    
    # ========== ایجاد سه کاربر ==========
    print("\n👤 ایجاد کاربران...")
    
    # کاربر ۱: مدیر سیستم
    admin = User(
        username="admin",
        full_name="  سید علی دانش",
        role="manager"
    )
    admin.set_password("admin123")
    db.session.add(admin)
    print("  ✅ کاربر مدیر: admin / admin123")
    
    # کاربر ۲: فروشنده ۱
    seller1 = User(
        username="seller1",
        full_name="حاجی علی",
        role="seller1"
    )
    seller1.set_password("seller1234")
    db.session.add(seller1)
    print("  ✅ کاربر فروشنده ۱: seller1 / seller1234")
    
    # کاربر ۳: فروشنده ۲
    seller2 = User(
        username="seller2",
        full_name="احمد رضا",
        role="seller2"
    )
    seller2.set_password("seller5678")
    db.session.add(seller2)
    print("  ✅ کاربر فروشنده ۲: seller2 / seller5678")
    
    # ========== ایجاد مشتری عمومی ==========
    print("\n👥 ایجاد مشتری عمومی...")
    general_customer = Customer(
        name="مشتری عمومی",
        phone="00000000000"
    )
    db.session.add(general_customer)
    print("  ✅ مشتری عمومی ایجاد شد")
    
    # ========== ایجاد موجودی نقدی اولیه ==========
    print("\n💰 ایجاد موجودی نقدی...")
    cash = CashBalance(
        amount=0,  # موجودی صفر
        last_updated=datetime.now()
    )
    db.session.add(cash)
    print("  ✅ موجودی نقدی: ۰ افغانی")
    
    # نهایی کردن تراکنش
    db.session.commit()
    
    print("\n" + "="*50)
    print("✅ دیتابیس با موفقیت ریست شد!")
    print("="*50)
    print("\n📋 اطلاعات کاربران:")
    print("  👤 مدیر سیستم: admin / admin123")
    print("  👤 فروشنده ۱: seller1 / seller1234")
    print("  👤 فروشنده ۲: seller2 / seller5678")
    print("\n📊 سایر موارد:")
    print("  👤 مشتری عمومی: موجود")
    print("  💰 موجودی نقدی: ۰ افغانی")
    print("="*50)