# app/license_config.py
import hashlib
import socket
import subprocess
from datetime import datetime, timedelta

# ==================== ثابت‌ها ====================
SECRET_KEY = "MY_SECRET_KEY_2025"
MAX_TRIAL_COUNT = 1
TRIAL_DAYS = 30
LICENSE_EXPIRE_DAYS = 365

# ==================== کش برای بهبود سرعت ====================
_hw_id_cache = None

# ==================== شناسه سخت‌افزاری ====================
def get_hardware_id():
    global _hw_id_cache
    if _hw_id_cache:
        return _hw_id_cache
    
    components = []
    
    try:
        result = subprocess.run(['wmic', 'baseboard', 'get', 'serialnumber'], capture_output=True, text=True, timeout=3)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1 and lines[1].strip():
            components.append(f"MB:{lines[1].strip()}")
    except:
        pass
    
    try:
        result = subprocess.run(['wmic', 'cpu', 'get', 'processorid'], capture_output=True, text=True, timeout=3)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1 and lines[1].strip():
            components.append(f"CPU:{lines[1].strip()}")
    except:
        pass
    
    try:
        result = subprocess.run(['vol', 'C:'], capture_output=True, text=True, timeout=3)
        for line in result.stdout.split('\n'):
            if 'Serial Number' in line or 'شماره سریال' in line:
                serial = line.split()[-1].strip()
                components.append(f"HDD:{serial}")
                break
    except:
        pass
    
    try:
        import uuid
        mac = uuid.getnode()
        components.append(f"MAC:{mac:012X}")
    except:
        pass
    
    components.append(f"HOST:{socket.gethostname()}")
    
    combined = "|".join(components)
    hw_id = hashlib.sha256(combined.encode()).hexdigest()[:16].upper()
    
    _hw_id_cache = hw_id
    return hw_id

# ==================== دریافت زمان واقعی (نسخه آفلاین فوق‌سریع) ====================
def get_real_time():
    """نسخه آفلاین - فقط زمان سیستم"""
    return datetime.now()

def get_real_date():
    real_time = get_real_time()
    return real_time.replace(hour=0, minute=0, second=0, microsecond=0)

def get_trial_expire_date():
    return get_real_date() + timedelta(days=TRIAL_DAYS)

def get_full_license_expire_date():
    return get_real_date() + timedelta(days=LICENSE_EXPIRE_DAYS)

def generate_license(hw_id=None):
    if hw_id is None:
        hw_id = get_hardware_id()
    raw = hw_id + SECRET_KEY
    license_key = hashlib.sha256(raw.encode()).hexdigest()[:20].upper()
    return license_key

def verify_license(hw_id, license_key):
    correct = generate_license(hw_id)
    return license_key == correct, correct

def can_use_trial(trial_count, last_trial_date=None):
    if trial_count >= MAX_TRIAL_COUNT:
        return False, f"تعداد مجاز استفاده از نسخه آزمایشی ({MAX_TRIAL_COUNT} بار) به پایان رسیده است"
    
    if last_trial_date:
        current_date = get_real_date()
        if hasattr(last_trial_date, 'date'):
            last_trial_date = last_trial_date.date()
        days_passed = (current_date - last_trial_date).days
        if days_passed < TRIAL_DAYS:
            remaining = TRIAL_DAYS - days_passed
            return False, f"برای استفاده مجدد از نسخه آزمایشی باید {remaining} روز دیگر صبر کنید"
    
    return True, "می‌توانید از نسخه آزمایشی استفاده کنید"