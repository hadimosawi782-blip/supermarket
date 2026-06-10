from app import create_app
from extensions import db
from app.models import User
from werkzeug.security import generate_password_hash

# اینجا اپ را می‌سازیم
app = create_app()

# با این دستور یک context باز می‌کنیم، کل کدهای دیتابیس باید داخل این بلاک باشد
with app.app_context():
    print("ایجاد/بررسی کاربران...")

    users = [
        {"username": "admin", "password": "1234", "full_name": "مدیر سیستم", "role": "admin"},
        {"username": "seller1", "password": "1111", "full_name": "فروشنده ۱", "role": "seller"},
        {"username": "seller2", "password": "2222", "full_name": "فروشنده ۲", "role": "seller"},
    ]

    for user_data in users:
        user = User.query.filter_by(username=user_data['username']).first()
        if not user:
            user = User(
                username=user_data['username'],
                password_hash=generate_password_hash(user_data['password']),
                full_name=user_data['full_name'],
                role=user_data['role']
            )
            db.session.add(user)

    db.session.commit()
    print("کاربران ایجاد شدند یا وجود داشتند.")
