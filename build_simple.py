# build_simple.py
import os
import sys
import shutil

print("=" * 60)
print("🔨 ساخت EXE - روش ساده")
print("=" * 60)

# پاک کردن پوشه‌های قبلی
for folder in ['build', 'dist', '__pycache__']:
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"✅ {folder} پاک شد")

# دستور ساده pyinstaller
command = (
    "pyinstaller "
    "--onefile "
    "--noconsole "
    "--name supermarket "
    "--add-data app;app "
    "--add-data instance;instance "
    "run.py"
)

print("\n🔨 در حال ساخت EXE...")
print("⏳ این فرآیند 2-3 دقیقه طول می‌کشد...")
print("-" * 60)

result = os.system(command)

if result == 0:
    print("\n" + "=" * 60)
    print("✅ EXE با موفقیت ساخته شد!")
    print("=" * 60)
    
    exe_path = os.path.join('dist', 'supermarket.exe')
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"📁 مسیر: {exe_path}")
        print(f"📦 حجم: {size:.2f} MB")
    else:
        print("❌ فایل EXE یافت نشد!")
else:
    print("\n❌ خطا در ساخت EXE!")
    print("🔍 خطا را بررسی کنید")

input("\n⏎ برای خروج Enter بزنید...")