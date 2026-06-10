import platform
import hashlib
import uuid

def get_hardware_id():
    # گرفتن اطلاعات پایه سیستم
    sys_info = platform.uname()
    raw_id = f"{sys_info.node}{sys_info.system}{sys_info.processor}{uuid.getnode()}"
    # هش کردن برای تولید یک رشته ثابت و کوتاه
    hw_id = hashlib.sha256(raw_id.encode()).hexdigest()
    return hw_id
