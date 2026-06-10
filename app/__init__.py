from flask import Flask
from .extensions import db, migrate, csrf, login_manager
from config import Config
import os
import sys
import jdatetime

# ✅ import توابع تاریخ شمسی
from .persian_date import to_persian_date, to_persian_datetime, get_current_persian_date

def create_app():
    app = Flask(__name__)

    # پشتیبانی از حالت EXE
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.abspath(os.path.dirname(__file__))

    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    csrf.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "main_bp.login"

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ✅ اضافه کردن فیلترهای تاریخ شمسی
    app.jinja_env.filters['persian_date'] = to_persian_date
    app.jinja_env.filters['persian_datetime'] = to_persian_datetime
    
    # ✅ اضافه کردن فیلتر jalali_date برای سازگاری با تمپلیت‌های قبلی
    app.jinja_env.filters['jalali_date'] = to_persian_date
    
    # ✅ اضافه کردن یک متغیر گلوبال برای تاریخ فعلی
    @app.context_processor
    def inject_persian_date():
        return dict(
            current_persian_date=get_current_persian_date(),
            now=jdatetime.datetime.now() if 'jdatetime' in sys.modules else None
        )

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app