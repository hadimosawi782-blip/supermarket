# build_exe.py
import os
import sys
import shutil
import subprocess

def build_exe():
    """ساخت EXE با تمام وابستگی‌ها"""
    
    print("=" * 70)
    print("🔨 ساخت EXE نهایی - سیستم مدیریت فروشگاه")
    print("=" * 70)
    
    # پاکسازی
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✅ پاک شد: {folder}")
    
    # ایجاد پوشه‌های لازم
    os.makedirs('instance', exist_ok=True)
    
    # ساخت دستور
    command = [
        'pyinstaller',
        '--onefile',
        '--noconsole',
        '--name', 'supermarket',
        '--add-data', 'app;app',
        '--add-data', 'instance;instance',
        '--hidden-import', 'app.license_config',
        '--hidden-import', 'app.license_manager',
        '--hidden-import', 'hashlib',
        '--hidden-import', 'socket',
        '--hidden-import', 'flask',
        '--hidden-import', 'flask_sqlalchemy',
        '--hidden-import', 'flask_login',
        'run.py'
    ]
    
    # اجرای دستور
    print("\n🔨 در حال ساخت EXE...")
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n✅ ساخت EXE با موفقیت انجام شد!")
        
        # چک کردن وجود فایل
        exe_path = os.path.join('dist', 'supermarket.exe')
        if os.path.exists(exe_path):
            size = os.path.getsize(exe_path) / (1024 * 1024)  # به مگابایت
            print(f"📁 فایل EXE ساخته شد: {exe_path}")
            print(f"📊 حجم فایل: {size:.2f} MB")
            
            # کپی فایل‌های لایسنس
            copy_license_files()
            create_batch_files()
            create_readme()
        else:
            print("❌ فایل EXE ساخته نشد!")
            print("\n📌 خطاهای احتمالی:")
            print(result.stderr)
    else:
        print("\n❌ خطا در ساخت EXE:")
        print(result.stderr)

def copy_license_files():
    """کپی فایل‌های لایسنس"""
    dist_folder = 'dist'
    if not os.path.exists(dist_folder):
        return
    
    license_files = ['license_core.py', 'generate_license_key.py', 'manage_license.py']
    for file in license_files:
        if os.path.exists(file):
            shutil.copy(file, os.path.join(dist_folder, file))
            print(f"📄 کپی شد: {file}")
    
    os.makedirs(os.path.join(dist_folder, 'licenses'), exist_ok=True)

def create_batch_files():
    """ایجاد فایل‌های bat"""
    with open('dist/run.bat', 'w') as f:
        f.write('@echo off\nstart supermarket.exe\npause')
    
    with open('dist/license_tools.bat', 'w') as f:
        f.write('@echo off\npython manage_license.py\npause')

def create_readme():
    """ایجاد README"""
    with open('dist/README.txt', 'w', encoding='utf-8') as f:
        f.write('سیستم مدیریت فروشگاه\nبرای اجرا: run.bat')

if __name__ == "__main__":
    build_exe()