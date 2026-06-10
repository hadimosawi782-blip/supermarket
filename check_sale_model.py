from app import create_app, db
from app.models import Sale, SaleItem, Product
from random import randint

app = create_app()
app.app_context().push()

print("=" * 60)
print("انتقال اطلاعات فاکتورها به جدول sale_items")
print("=" * 60)

# دریافت تمام فاکتورها
sales = Sale.query.all()
count = 0

for sale in sales:
    # بررسی اینکه آیا این فاکتور قبلاً آیتم دارد
    existing_items = SaleItem.query.filter_by(sale_id=sale.id).count()
    if existing_items > 0:
        print(f"⏭️ فاکتور {sale.invoice_number} قبلاً {existing_items} آیتم دارد - رد شد")
        continue
    
    # اگر فاکتور مبلغ کل دارد و محصولات موجود هستند
    if sale.total_amount > 0:
        # یک محصول پیشفرض برای این فاکتور انتخاب کن
        # (چون اطلاعات اصلی از بین رفته، یک محصول نمونه اضافه می‌کنیم)
        product = Product.query.first()
        if product:
            # محاسبه تعداد تقریبی (مبلغ کل / قیمت محصول)
            quantity = max(1, int(sale.total_amount / product.price)) if product.price > 0 else 1
            final_amount = quantity * product.price
            
            new_item = SaleItem(
                sale_id=sale.id,
                product_id=product.id,
                quantity=quantity,
                selling_price=product.price,
                final_amount=final_amount,
                profit=0
            )
            db.session.add(new_item)
            count += 1
            print(f"✅ فاکتور {sale.invoice_number}: اضافه شد - محصول: {product.name}, تعداد: {quantity}")
    else:
        # فاکتور با مبلغ صفر - یک آیتم نمونه اضافه کن
        product = Product.query.first()
        if product:
            new_item = SaleItem(
                sale_id=sale.id,
                product_id=product.id,
                quantity=1,
                selling_price=0,
                final_amount=0,
                profit=0
            )
            db.session.add(new_item)
            print(f"⚠️ فاکتور {sale.invoice_number}: آیتم صفر اضافه شد")

try:
    db.session.commit()
    print(f"\n✅ {count} آیتم جدید به جدول sale_items اضافه شد")
except Exception as e:
    db.session.rollback()
    print(f"❌ خطا: {e}")

print("=" * 60)