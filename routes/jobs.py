from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from extensions import db
from models import Job, Candidate, Application
import os

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/jobs")
def jobs():

    keyword = request.args.get("keyword", "")
    location = request.args.get("location", "")
    category = request.args.get("category", "")

    query = Job.query

    if keyword:
        query = query.filter(Job.title.contains(keyword))

    if location:
        query = query.filter(Job.location.contains(location))

    if category:
        query = query.filter(Job.category.contains(category))

    jobs = query.order_by(Job.created_at.desc()).all()

    return render_template(
        "jobs.html",
        jobs=jobs
    )


@jobs_bp.route("/job/<int:id>")
def job_details(id):

    job = Job.query.get_or_404(id)

    return render_template(
        "job_details.html",
        job=job
    )


@jobs_bp.route("/apply/<int:job_id>", methods=["GET", "POST"])
def apply(job_id):

    job = Job.query.get_or_404(job_id)

    if request.method == "POST":

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        nationality = request.form.get("nationality")

        filename = ""

        cv = request.files.get("cv")

        if cv and cv.filename:

            filename = secure_filename(cv.filename)

            upload_folder = current_app.config["UPLOAD_FOLDER"]

            os.makedirs(upload_folder, exist_ok=True)

            cv.save(
                os.path.join(
                    upload_folder,
                    filename
                )
            )

        candidate = Candidate(
            full_name=full_name,
            email=email,
            phone=phone,
            nationality=nationality,
            cv_file=filename
        )

        db.session.add(candidate)
        db.session.commit()

        application = Application(
            candidate_id=candidate.id,
            job_id=job.id,
            status="Pending"
        )

        db.session.add(application)
        db.session.commit()

        flash(
            "Application submitted successfully.",
            "success"
        )

        return redirect(
            url_for("jobs.jobs")
        )

    return render_template(
        "apply.html",
        job=job
    )

    
