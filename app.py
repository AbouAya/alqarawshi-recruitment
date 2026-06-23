from flask import Flask
from config import Config
from extensions import db 
from extensions import login_manager, migrate

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

# Import models
from models import *

# Register Blueprints
from routes.website import website_bp
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.jobs import jobs_bp
from routes.employer import employer_bp
from routes.contact import contact_bp

app.register_blueprint(website_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(jobs_bp)
app.register_blueprint(employer_bp)
app.register_blueprint(contact_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
 
from models import User

with app.app_context():

    db.create_all()

    admin = User.query.filter_by(username="admin").first()

    if not admin:

        admin = User(
            username="admin",
            email="admin@alkarawchi.com",
            role="admin"
        )

        admin.set_password("admin123")

        db.session.add(admin)
        db.session.commit()

        print("Admin account created.")


if __name__ == "__main__":
    app.run(debug=True)

    










