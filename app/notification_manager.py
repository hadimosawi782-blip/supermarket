# app/notification_manager.py
from datetime import datetime, timedelta
from app import db
from app.models import Notification, Product

class NotificationManager:
    """مدیریت اعلان‌های سیستم"""
    
    LOW_STOCK_THRESHOLD = 5  # موجودی کمتر از 5
    EXPIRY_DAYS_THRESHOLD = 30  # نزدیک انقضا کمتر از 30 روز
    
    @staticmethod
    def check_low_stock():
        """بررسی محصولات با موجودی کم و ایجاد اعلان"""
        created_count = 0
        try:
            products = Product.query.filter(Product.quantity < NotificationManager.LOW_STOCK_THRESHOLD).all()
            
            for product in products:
                # پاک کردن اعلان‌های قدیمی برای این محصول
                Notification.query.filter_by(
                    product_id=product.id,
                    type='low_stock'
                ).delete()
                
                # ایجاد اعلان جدید
                is_urgent = product.quantity < 2
                notification = Notification(
                    type='low_stock',
                    title=f'⚠️ موجودی کم: {product.name}',
                    message=f'موجودی محصول "{product.name}" به {product.quantity} {product.unit} رسیده است.',
                    product_id=product.id,
                    product_name=product.name,
                    current_quantity=product.quantity,
                    min_stock=NotificationManager.LOW_STOCK_THRESHOLD,
                    is_urgent=is_urgent,
                    created_at=datetime.utcnow()
                )
                db.session.add(notification)
                created_count += 1
            
            db.session.commit()
            return created_count
        except Exception as e:
            print(f"❌ خطا در بررسی موجودی کم: {e}")
            return 0
    
    @staticmethod
    def check_expiring_products():
        """بررسی محصولات نزدیک به انقضا و ایجاد اعلان"""
        created_count = 0
        try:
            today = datetime.now().date()
            expiry_threshold = today + timedelta(days=NotificationManager.EXPIRY_DAYS_THRESHOLD)
            
            products = Product.query.filter(
                Product.expiry_date.isnot(None),
                Product.expiry_date <= expiry_threshold,
                Product.expiry_date >= today
            ).all()
            
            for product in products:
                days_remaining = (product.expiry_date - today).days
                
                # پاک کردن اعلان‌های قدیمی برای این محصول
                Notification.query.filter_by(
                    product_id=product.id,
                    type='expiring'
                ).delete()
                
                # ایجاد اعلان جدید
                is_urgent = days_remaining < 7
                notification = Notification(
                    type='expiring',
                    title=f'📅 نزدیک به انقضا: {product.name}',
                    message=f'محصول "{product.name}" در تاریخ {product.expiry_date.strftime("%Y-%m-%d")} منقضی می‌شود. ({days_remaining} روز باقی‌مانده)',
                    product_id=product.id,
                    product_name=product.name,
                    expiry_date=product.expiry_date,
                    days_remaining=days_remaining,
                    is_urgent=is_urgent,
                    created_at=datetime.utcnow()
                )
                db.session.add(notification)
                created_count += 1
            
            db.session.commit()
            return created_count
        except Exception as e:
            print(f"❌ خطا در بررسی محصولات نزدیک انقضا: {e}")
            return 0
    
    @staticmethod
    def get_unread_count():
        """تعداد اعلان‌های خوانده نشده"""
        return Notification.query.filter_by(is_read=False).count()
    
    @staticmethod
    def get_urgent_count():
        """تعداد اعلان‌های فوری"""
        return Notification.query.filter_by(is_read=False, is_urgent=True).count()
    
    @staticmethod
    def get_all_notifications():
        """دریافت همه اعلان‌ها"""
        return Notification.query.order_by(
            Notification.created_at.desc()
        ).all()