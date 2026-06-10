from flask import Flask
from flask_migrate import Migrate, upgrade
from extensions import db, csrf, login_manager
from config import Config

# وارد کردن مدل‌ها تا Flask-Migrate آنها را بشناسد
from app.models import Product, Customer, Sale, SaleItem, DebtPayment, DailyExpense, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # اتصال افزونه‌ها
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    migrate = Migrate(app, db)

    return app


app = create_app()

# دستور ساده برای ایجاد جدول‌ها با یک فرمان پایتون
@app.cli.command("init_db")
def init_db():
    """ایجاد تمام جدول‌ها در دیتابیس"""
    with app.app_context():
        db.create_all()
        print("✅ All tables created successfully!")


# برای اجرای migrate و upgrade از CLI هم می‌توانی استفاده کنی:
# flask db init
# flask db migrate -m "initial migration"
# flask db upgrade
