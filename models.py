from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


#class users
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="admin")
    active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# ============================
# Employers
# ============================

class Employer(db.Model):
    __tablename__ = "employers"

    id = db.Column(db.Integer, primary_key=True)

    company_name = db.Column(db.String(200), nullable=False)

    contact_person = db.Column(db.String(120))

    email = db.Column(db.String(120), unique=True, nullable=False)

    phone = db.Column(db.String(50))

    password = db.Column(db.String(255))

    website = db.Column(db.String(200))

    logo = db.Column(db.String(200))

    address = db.Column(db.String(250))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    jobs = db.relationship(
        "Job",
        backref="employer",
        lazy=True,
        cascade="all, delete"
    )
    
class Job(db.Model):

    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    location = db.Column(db.String(100))

    salary = db.Column(db.String(100))

    category = db.Column(db.String(100))

    job_type = db.Column(db.String(50))

    description = db.Column(db.Text)

    requirements = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employer_id = db.Column(
        db.Integer,
        db.ForeignKey("employers.id")
    )

    applications = db.relationship(
        "Application",
        backref="job",
        lazy=True,
        cascade="all, delete"
    )
        
class Candidate(db.Model):

    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(150))

    email = db.Column(db.String(150))

    phone = db.Column(db.String(50))

    nationality = db.Column(db.String(80))

    cv_file = db.Column(db.String(250))

    photo = db.Column(db.String(250))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship(
        "Application",
        backref="candidate",
        lazy=True,
        cascade="all, delete"
    )
    
class Application(db.Model):

    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey("candidates.id")
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id")
    )

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    applied_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
class ContactMessage(db.Model):

    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150))

    email = db.Column(db.String(150))

    phone = db.Column(db.String(50))

    subject = db.Column(db.String(200))

    message = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    
class EmployerRequest(db.Model):

    __tablename__ = "employer_requests"

    id = db.Column(db.Integer, primary_key=True)

    company = db.Column(db.String(200))

    contact_person = db.Column(db.String(150))

    email = db.Column(db.String(150))

    phone = db.Column(db.String(50))

    workers_needed = db.Column(db.Integer)

    position = db.Column(db.String(150))

    message = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
