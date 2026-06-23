from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

from extensions import db
from models import Employer

employer_bp = Blueprint("employer", __name__)

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