# manage_license.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
مدیریت لایسنس برنامه
"""

import sys
from app import create_app
from app.license_manager import LicenseManager
from app.license_config import get_hardware_id, generate_license  # اضافه شد

def print_help():
    print("""
مدیریت لایسنس برنامه
----------------------
دستورات موجود:
    info                 نمایش اطلاعات لایسنس
    create [days]        ایجاد لایسنس آزمایشی (پیش‌فرض: 365 روز)
    activate             فعال‌سازی از روی فایل license.key
    file                 نمایش اطلاعات فایل لایسنس
    hwid                 نمایش HW ID فعلی
    check [license]      بررسی یک کد لایسنس
    help                 نمایش این راهنما
    """)

def main():
    if len(sys.argv) < 2 or sys.argv[1] == 'help':
        print_help()
        return

    app = create_app()
    with app.app_context():
        command = sys.argv[1]
        
        if command == 'info':
            LicenseManager.show_license_info()
            
        elif command == 'create':
            days = 30
            if len(sys.argv) > 2:
                try:
                    days = int(sys.argv[2])
                except:
                    pass
            success, msg = LicenseManager.create_trial_license(days)
            print(msg)
            
        elif command == 'activate':
            success, msg = LicenseManager.activate_license_from_file()
            print(msg)
            
        elif command == 'file':
            file_path = LicenseManager.find_license_file()
            if file_path:
                print(f"📄 مسیر فایل: {file_path}")
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                print(f"🔑 محتوا: {content}")
                
                hw = get_hardware_id()  # از config استفاده کن
                required = generate_license(hw)  # از config استفاده کن
                print(f"✅ لایسنس مورد نیاز: {required}")
                if content == required:
                    print("✅ فایل معتبر است")
                else:
                    print("❌ فایل نامعتبر است")
            else:
                print("❌ فایل لایسنس یافت نشد")
                
        elif command == 'hwid':
            hw = get_hardware_id()
            print(f"💻 HW ID این سیستم: {hw}")
            print(f"🔑 لایسنس مربوطه: {generate_license(hw)}")
            
        elif command == 'check':
            if len(sys.argv) < 3:
                print("❌ لطفاً کد لایسنس را وارد کنید")
                return
            license_key = sys.argv[2]
            hw = get_hardware_id()
            required = generate_license(hw)
            if license_key == required:
                print("✅ لایسنس معتبر است")
            else:
                print("❌ لایسنس نامعتبر است")
                print(f"   کد صحیح: {required}")
                
        else:
            print(f"❌ دستور نامشخص: {command}")
            print_help()

if __name__ == "__main__":
    main()