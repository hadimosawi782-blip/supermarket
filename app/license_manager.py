# app/license_manager.py
from datetime import datetime
from app import db
from app.models import License
from app.license_config import get_hardware_id, generate_license, get_full_license_expire_date

class LicenseManager:
    # ... سایر متدها ...
    
    @staticmethod
    def create_trial_license():
        """ایجاد یا تمدید لایسنس آزمایشی با محدودیت"""
        try:
            hw = LicenseManager.get_hardware_id()
            existing_license = License.query.first()
            
            if existing_license:
                # بررسی امکان استفاده مجدد
                can_use, msg = existing_license.can_use_trial()
                if not can_use:
                    return False, msg
                
                # تمدید لایسنس آزمایشی
                success, msg = existing_license.add_trial()
                return success, msg
            else:
                # ایجاد لایسنس آزمایشی جدید
                from app.license_config import get_trial_expire_date
                
                new_license = License(
                    hw_id=hw,
                    expire_at=get_trial_expire_date(),
                    trial_count=1,
                    last_trial_date=datetime.utcnow()
                )
                db.session.add(new_license)
                db.session.commit()
                return True, "لایسنس آزمایشی 30 روزه فعال شد (فقط یک بار)"
            
        except Exception as e:
            return False, f"خطا: {str(e)}"
    
    @staticmethod
    def activate_license_from_file():
        """فعال‌سازی لایسنس کامل از فایل"""
        file_valid, msg = LicenseManager.check_license_from_file()
        if not file_valid:
            return False, msg
        
        hw = LicenseManager.get_hardware_id()
        existing_license = License.query.first()
        
        if existing_license:
            # فعال‌سازی لایسنس کامل
            success, msg = existing_license.activate_full_license()
            return success, msg
        else:
            # ایجاد لایسنس کامل جدید
            new_license = License(
                hw_id=hw,
                expire_at=get_full_license_expire_date()
            )
            db.session.add(new_license)
            db.session.commit()
            return True, "لایسنس کامل با موفقیت فعال شد"
    
    @staticmethod
    def show_license_info():
        """نمایش اطلاعات لایسنس"""
        print("\n" + "=" * 60)
        print("سیستم مدیریت لایسنس")
        print("=" * 60)
        
        hw_id = LicenseManager.get_hardware_id()
        required_license = LicenseManager.generate_license(hw_id)
        
        print(f"🔹 شناسه سخت‌افزاری: {hw_id}")
        print(f"🔹 لایسنس مورد نیاز: {required_license}")
        
        db_valid, db_msg = LicenseManager.check_license_from_db()
        print(f"\n📊 وضعیت دیتابیس: {db_msg}")
        
        if db_valid:
            license = License.query.first()
            print(f"   📅 تاریخ انقضا: {license.expire_at.strftime('%Y-%m-%d')}")
            print(f"   🔄 دفعات استفاده از آزمایشی: {license.trial_count} بار")
        
        file_valid, file_msg = LicenseManager.check_license_from_file()
        print(f"📄 وضعیت فایل: {file_msg}")
        
        print("=" * 60)
        return db_valid or file_valid