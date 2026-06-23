from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os

from extensions import db
from models import Employer

employer_bp = Blueprint("employer", __name__)

@employer_bp.route("/employer/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        employer = Employer.query.filter_by(
            email=request.form["email"]
        ).first()

        if employer is None:

            flash("Invalid email.", "danger")
            return redirect(url_for("employer.login"))

        if not employer.check_password(request.form["password"]):

            flash("Incorrect password.", "danger")
            return redirect(url_for("employer.login"))

        if not employer.approved:

            flash(
                "Your company is awaiting admin approval.",
                "warning"
            )
            return redirect(url_for("employer.login"))

        if not employer.active:

            flash(
                "Your account has been disabled.",
                "danger"
            )
            return redirect(url_for("employer.login"))

        session["employer_id"] = employer.id

        flash(
            f"Welcome {employer.company_name}",
            "success"
        )

        return redirect(url_for("employer.dashboard"))

    return render_template("employer/login.html")

@employer_bp.route("/employer/logout")
def logout():

    session.pop("employer_id", None)

    flash("Logged out successfully.", "success")

    return redirect(url_for("website.home"))

@employer_bp.route("/employer/dashboard")
def dashboard():

    if "employer_id" not in session:

        return redirect(url_for("employer.login"))

    employer = Employer.query.get_or_404(
        session["employer_id"]
    )

    jobs = Job.query.filter_by(
        employer_id=employer.id
    ).all()

    return render_template(
        "employer/dashboard.html",
        employer=employer,
        jobs=jobs
    )

@employer_bp.route("/employer/register", methods=["GET", "POST"])
def register():

required = [
    "company_name",
    "contact_person",
    "email",
    "password",
    "confirm_password"
]

for field in required:
    if not request.form.get(field):
        flash(f"{field.replace('_',' ').title()} is required.", "danger")
        return redirect(url_for("employer.register"))

    if request.method == "POST":

        if Employer.query.filter_by(
            email=request.form["email"]
        ).first():

            flash("Email already exists.", "danger")
            return redirect(url_for("employer.register"))

        if request.form["password"] != request.form["confirm_password"]:

            flash("Passwords do not match.", "danger")
            return redirect(url_for("employer.register"))

        employer = Employer(

            company_name=request.form["company_name"],

            contact_person=request.form["contact_person"],

            email=request.form["email"],

            phone=request.form["phone"],

            website=request.form["website"],

            industry=request.form["industry"],

            company_size=request.form["company_size"],

            country=request.form["country"],

            city=request.form["city"],

            description=request.form["description"]

        )

        employer.set_password(request.form["password"])

            if len(request.form["password"]) < 8:
                flash(
                    "Password must contain at least 8 characters.",
                    "danger"
                )
                return redirect(url_for("employer.register"))
        logo = request.files.get("logo")

        if logo and logo.filename:

            if not allowed_file(logo.filename):

                flash(
                    "Logo must be PNG, JPG, JPEG or WEBP.",
                    "danger"
                )

                return redirect(
                    url_for("employer.register")
                )

            import uuid

                filename = (
                    str(uuid.uuid4())
                    + "_"
                    + secure_filename(logo.filename)
                )

                from flask import current_app

                upload_folder = current_app.config["UPLOAD_FOLDER"]

            logo.save(
                os.path.join(
                    upload_folder,
                    filename
                )
            )
            
            employer.logo = filename

        db.session.add(employer)

        db.session.commit()

        flash(
            "Registration submitted successfully. Waiting for admin approval.",
            "success"
        )

        return redirect(url_for("website.home"))

    return render_template("employer/register.html")