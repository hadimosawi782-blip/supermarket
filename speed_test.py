# speed_test.py
import time
from app import create_app
from app.license_config import get_hardware_id, get_real_time

app = create_app()

# تست 1: HW ID
start = time.time()
hw = get_hardware_id()
print(f"⏱️ HW ID: {time.time() - start:.3f} ثانیه")

# تست 2: زمان واقعی
start = time.time()
rt = get_real_time()
print(f"⏱️ زمان واقعی: {time.time() - start:.3f} ثانیه")

# تست 3: اتصال به دیتابیس
start = time.time()
with app.app_context():
    from app.models import License
    license = License.query.first()
print(f"⏱️ دیتابیس: {time.time() - start:.3f} ثانیه")