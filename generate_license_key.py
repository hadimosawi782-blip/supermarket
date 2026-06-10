#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
تولید کننده لایسنس - نسخه یکپارچه
"""

import sys
import os
from datetime import datetime, timedelta
from app.license_config import get_hardware_id, generate_license, verify_license

def format_license_key(key):
    """تبدیل کد لایسنس به فرمت خوانا"""
    if len(key) >= 20:
        return '-'.join([key[i:i+4] for i in range(0, 20, 4)])
    return key

def main():
    print("\n" + "=" * 70)
    print("🔐 **تولید کننده لایسنس - نسخه یکپارچه**")
    print("=" * 70)
    
    # نمایش HW ID فعلی
    current_hwid = get_hardware_id()
    print(f"\n💻 HW ID این سیستم: {current_hwid}")
    print(f"🔑 لایسنس این سیستم: {generate_license(current_hwid)}")
    print("-" * 70)
    
    # دریافت HW ID
    if len(sys.argv) > 1:
        hw_id = sys.argv[1].upper()
    else:
        hw_id = input("🔹 HW ID را وارد کنید [خالی برای سیستم فعلی]: ").strip().upper()
        if not hw_id:
            hw_id = current_hwid
    
    # دریافت مدت اعتبار
    days = 365  # پیش‌فرض 1 سال
    if len(sys.argv) > 2:
        try:
            days = int(sys.argv[2])
        except:
            pass
    
    # تولید لایسنس
    license_key = generate_license(hw_id)
    
    # بررسی صحت
    is_valid, correct_key = verify_license(hw_id, license_key)
    
    print("\n" + "✅" * 35)
    print("📋 **لایسنس تولید شد**")
    print("✅" * 35)
    
    print(f"\n📋 HW ID: {hw_id}")
    print(f"🔑 لایسنس: {license_key}")
    print(f"🔑 فرمت شده: {format_license_key(license_key)}")
    
    if is_valid:
        print(f"\n✅ لایسنس صحیح است")
    else:
        print(f"\n❌ خطا! این لایسنس برای این HW ID صحیح نیست")
        print(f"   لایسنس صحیح: {correct_key}")
    
    # ایجاد فایل license.key
    with open('license.key', 'w') as f:
        f.write(license_key)
    
    print(f"\n📁 فایل license.key ایجاد شد")
    print(f"📅 مدت اعتبار: {days} روز")
    print(f"📆 تاریخ انقضا: {(datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()