from app import create_app
from extensions import db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    admin = User(username="admin", password_hash=generate_password_hash("1234"))
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin user created: username=admin, password=1234")
