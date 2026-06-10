import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def create_and_setup_app():
    from app import create_app
    from app.models import db, User

    app = create_app()

    with app.app_context():
        try:
            db.create_all()

            if not User.query.filter_by(username='admin').first():
                admin = User(
                    username='admin',
                    full_name='مدیر سیستم',
                    role='admin'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()

        except Exception as e:
            print(f"Database setup error: {e}")

    return app


# این خط باید خارج از __main__ باشد
app = create_and_setup_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )