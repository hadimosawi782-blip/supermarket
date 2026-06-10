# init_db.py
import os
from datetime import datetime, timedelta
from app import create_app
from app.models import db, User, License

app = create_app()

def init_db():
    with app.app_context():
        db.create_all()  # ایجاد جداول
        # اضافه کردن کاربران پیش‌فرض
        users_data = [
            ("admin", "1234", "مدیر سیستم"),
            ("seller1", "1111", "فروشنده ۱"),
            ("seller2", "2222", "فروشنده ۲"),
        ]
        for username, password, full_name in users_data:
            if not User.query.filter_by(username=username).first():
                user = User(username=username, full_name=full_name)
                user.set_password(password)
                db.session.add(user)

        # لایسنس یک‌ساله
        if not License.query.first():
            license = License(expire_at=datetime.utcnow() + timedelta(days=365))
            db.session.add(license)

        db.session.commit()
        print("✅ دیتابیس و کاربران با موفقیت ایجاد شدند.")

if __name__ == "__main__":
    init_db()
