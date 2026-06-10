# license_core.py
import os
import sys
from app.license_config import get_hardware_id, generate_license, verify_license

def get_app_base_path():
    """دریافت مسیر صحیح برنامه"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def find_license_file():
    """پیدا کردن فایل لایسنس"""
    base_path = get_app_base_path()
    
    possible_locations = [
        os.path.join(base_path, "instance", "license.key"),
        os.path.join(base_path, "license.key"),
        os.path.join("instance", "license.key"),
        "license.key",
    ]
    
    for location in possible_locations:
        if os.path.exists(location):
            return location
    
    return None

def check_license():
    """بررسی لایسنس"""
    license_path = find_license_file()
    
    if not license_path:
        print(f"❌ فایل لایسنس یافت نشد!")
        return False
    
    try:
        with open(license_path, "r") as f:
            stored_key = f.read().strip()
        
        hw = get_hardware_id()
        valid_key = generate_license(hw)
        
        if stored_key == valid_key:
            print(f"✅ لایسنس معتبر است")
            return True
        else:
            print(f"❌ لایسنس نامعتبر است")
            print(f"   شناسه سیستم: {hw}")
            print(f"   لایسنس مورد نیاز: {valid_key}")
            return False
            
    except Exception as e:
        print(f"❌ خطا: {e}")
        return False

def show_license_info():
    """نمایش اطلاعات لایسنس"""
    print("\n" + "=" * 60)
    print("سیستم مدیریت لایسنس")
    print("=" * 60)
    
    hw_id = get_hardware_id()
    required_license = generate_license(hw_id)
    
    print(f"🔹 شناسه سخت‌افزاری: {hw_id}")
    print(f"🔹 لایسنس مورد نیاز: {required_license}")
    
    is_valid = check_license()
    
    if is_valid:
        print(f"\n✅ سیستم فعال است!")
    else:
        print(f"\n⚠️  برای فعال‌سازی:")
        print(f"   فایل 'license.key' با محتوای:")
        print(f"   {required_license}")
    
    print("=" * 60)
    return is_valid

if __name__ == "__main__":
    show_license_info()