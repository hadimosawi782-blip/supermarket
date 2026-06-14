import os
import sys

# مسیر دیتابیس
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

LOCAL_DB = f"sqlite:///{os.path.join(BASE_DIR, 'supermarket.db')}"

# اگر DATABASE_URL وجود داشت از آن استفاده کن
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )

class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "YOUR-SECRET"
    )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or LOCAL_DB

    SQLALCHEMY_TRACK_MODIFICATIONS = False