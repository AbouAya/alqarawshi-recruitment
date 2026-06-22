from app import app
from extensions import db
from models import User

with app.app_context():

    if not User.query.filter_by(username="admin").first():

        admin = User(
            username="admin",
            email="info@alqarawshi.com",
            role="admin"
        )

        admin.set_password("Admin@2026")

        db.session.add(admin)

        db.session.commit()

        print("Admin created")

    else:
        print("Admin already exists")