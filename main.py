import sys
import os
import traceback

# اضافه کردن پوشه app به مسیر
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def create_and_setup_app():
    """ایجاد app و setup دیتابیس"""
    from app import create_app
    from app.models import db, User
    
    app = create_app()
    
    with app.app_context():
        try:
            # ایجاد همه tables
            db.create_all()
            print("✅ Database tables created")
            
            # ایجاد کاربر admin
            if not User.query.filter_by(username='admin').first():
                admin = User(
                    username='admin',
                    full_name='مدیر سیستم',
                    role='admin'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✅ Admin: admin / admin123")
            
        except Exception as e:
            print(f"⚠️ Database setup: {str(e)}")
    
    return app

if __name__ == "__main__":
    try:
        app = create_and_setup_app()
        
        print("\n🚀 Supermarket Management System")
        print("🌐 http://127.0.0.1:5000")
        print("🔑 admin / admin123")
        
        app.run(debug=False, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        input("Press Enter to exit...")
