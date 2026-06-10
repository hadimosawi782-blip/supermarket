from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_login import LoginManager

# ایجاد اشیا
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()

# user_loader function
@login_manager.user_loader
def load_user(user_id):
    """بارگذاری کاربر از دیتابیس"""
    from app.models import User  # import here to avoid circular import
    return User.query.get(int(user_id))

# تابع برای تنظیم extensions با app
def init_extensions(app):
    """تنظیم همه extensions با برنامه"""
    
    # تنظیم SQLAlchemy با app
    db.init_app(app)
    
    # اعمال تنظیمات چند کاربری به SQLAlchemy
    if 'SQLALCHEMY_ENGINE_OPTIONS' in app.config:
        pass
    else:
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'connect_args': {
                'check_same_thread': False,
                'timeout': 30
            }
        }
    
    # تنظیم سایر extensions
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    
    # تنظیمات login manager
    login_manager.login_view = 'main.login'  # مطمئن شوید این endpoint صحیح است
    login_manager.login_message = 'لطفا وارد شوید'
    login_manager.login_message_category = 'info'
    
    return app
