# run.py
import sys
import os
import threading
import webbrowser
from app import create_app

app = create_app()

def resource_path(relative_path):
    """دریافت مسیر صحیح فایل‌ها در حالت EXE"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_database_path():
    """ایجاد دیتابیس در پوشه کاربر (نه داخل EXE)"""
    # دیتابیس را در پوشه کاربر ذخیره کن
    appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
    db_dir = os.path.join(appdata, 'SupermarketApp')
    
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    db_path = os.path.join(db_dir, 'supermarket.db')
    
    # اگر دیتابیس در پوشه برنامه وجود دارد، کپی کن
    local_db = 'supermarket.db'
    if os.path.exists(local_db) and not os.path.exists(db_path):
        import shutil
        shutil.copy2(local_db, db_path)
    
    return db_path

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 سیستم مدیریت فروشگاه")
    print("=" * 60)
    print(f"📂 مسیر دیتابیس: {get_database_path()}")
    print(f"📦 حالت: {'EXE' if getattr(sys, 'frozen', False) else 'توسعه'}")
    print("-" * 60)
    print("🌐 آدرس: http://127.0.0.1:5000")
    print("=" * 60)
    
    threading.Timer(2.0, open_browser).start()
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False
    )