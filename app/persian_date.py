# app/persian_date.py
import jdatetime
from datetime import datetime

def to_persian_date(date_obj):
    """تبدیل تاریخ میلادی به شمسی"""
    if not date_obj:
        return "---"
    
    # اگر datetime است به date تبدیل کن
    if isinstance(date_obj, datetime):
        date_obj = date_obj.date()
    
    try:
        # تبدیل به شمسی
        persian_date = jdatetime.date.fromgregorian(date=date_obj)
        return persian_date.strftime("%Y/%m/%d")
    except:
        return "---"

def to_persian_datetime(datetime_obj):
    """تبدیل تاریخ و زمان میلادی به شمسی"""
    if not datetime_obj:
        return "---"
    
    try:
        persian_datetime = jdatetime.datetime.fromgregorian(datetime=datetime_obj)
        return persian_datetime.strftime("%Y/%m/%d - %H:%M")
    except:
        return "---"

def get_current_persian_date():
    """دریافت تاریخ فعلی شمسی"""
    try:
        return jdatetime.date.today().strftime("%Y/%m/%d")
    except:
        return "---"

def get_current_persian_datetime():
    """دریافت تاریخ و زمان فعلی شمسی"""
    try:
        return jdatetime.datetime.now().strftime("%Y/%m/%d - %H:%M")
    except:
        return "---"