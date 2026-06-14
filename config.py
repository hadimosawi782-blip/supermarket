import os
import sys

# تشخیص Render
IS_RENDER = os.environ.get("RENDER") == "true"

# دیتابیس آنلاین
if IS_RENDER:
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql://",
            1
        )

# دیتابیس آفلاین
else:
    if getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(sys.executable)
    else:
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'supermarket.db')}"

class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "YOUR-SECRET"
    )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False