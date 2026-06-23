from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db
from models import (
    User,
    Job,
    Employer,
    Candidate,
    Application,
    ContactMessage,
    EmployerRequest,
)

admin_bp = Blueprint("admin", __name__)


# -------------------------
# Admin Login
# -------------------------

@admin_bp.route("/admin/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):

            login_user(user)

            flash("Welcome back.", "success")

            return redirect(url_for("admin.dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("auth/login.html")


# -------------------------
# Logout
# -------------------------

@admin_bp.route("/admin/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.", "success")

    return redirect(url_for("website.home"))


# -------------------------
# Dashboard
# -------------------------

@admin_bp.route("/admin/dashboard")
@login_required
def dashboard():

    total_jobs = Job.query.count()

    total_candidates = Candidate.query.count()

    total_employers = Employer.query.count()

    total_applications = Application.query.count()

    latest_jobs = Job.query.order_by(
        Job.created_at.desc()
    ).limit(5).all()

    latest_candidates = Candidate.query.order_by(
        Candidate.created_at.desc()
    ).limit(5).all()

    return render_template(
        "admin/dashboard.html",

        total_jobs=total_jobs,
        total_candidates=total_candidates,
        total_employers=total_employers,
        total_applications=total_applications,

        latest_jobs=latest_jobs,
        latest_candidates=latest_candidates
    )


# -------------------------
# Candidates
# -------------------------

@admin_bp.route("/admin/candidates")
@login_required
def candidates():

    candidates = Candidate.query.order_by(
        Candidate.created_at.desc()
    ).all()

    return render_template(
        "admin/candidates.html",
        candidates=candidates,
    )

@admin_bp.route("/admin/employer/<int:id>/approve")
@login_required
def approve_employer(id):

    employer = Employer.query.get_or_404(id)

    employer.approved = True

    db.session.commit()

    flash(
        "Employer approved successfully.",
        "success"
    )

    return redirect(url_for("admin.employers"))

# -------------------------
# Employers
# -------------------------

@admin_bp.route("/admin/employers")
@login_required
def employers():

    employers = Employer.query.order_by(
        Employer.created_at.desc()
    ).all()

    return render_template(
        "admin/employers.html",
        employers=employers,
    )


# -------------------------
# Contact Messages
# -------------------------

@admin_bp.route("/admin/messages")
@login_required
def messages():

    messages = ContactMessage.query.order_by(
        ContactMessage.created_at.desc()
    ).all()

    return render_template(
        "admin/messages.html",
        messages=messages,
    )


# -------------------------
# Employer Requests
# -------------------------

@admin_bp.route("/admin/employer-requests")
@login_required
def employer_requests():

    requests = EmployerRequest.query.order_by(
        EmployerRequest.created_at.desc()
    ).all()

    return render_template(
        "admin/employer_requests.html",
        requests=requests,
    )
# ===========================
# JOBS MANAGEMENT
# ===========================

@admin_bp.route("/admin/jobs")
@login_required
def manage_jobs():

    jobs = Job.query.order_by(Job.id.desc()).all()

    return render_template(
        "admin/jobs.html",
        jobs=jobs
    )

@admin_bp.route("/admin/jobs/add", methods=["GET","POST"])
@login_required
def add_job():

    if request.method == "POST":

        job = Job(

            title=request.form["title"],

            location=request.form["location"],

            salary=request.form["salary"],

            category=request.form["category"],

            job_type=request.form["job_type"],

            description=request.form["description"],

            requirements=request.form["requirements"]

        )

        db.session.add(job)

        db.session.commit()

        flash("Job created successfully.","success")

        return redirect(url_for("admin.manage_jobs"))

    return render_template("admin/add_job.html")

@admin_bp.route("/admin/jobs/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_job(id):

    job = Job.query.get_or_404(id)

    if request.method == "POST":

        job.title = request.form["title"]
        job.location = request.form["location"]
        job.salary = request.form["salary"]
        job.category = request.form["category"]
        job.job_type = request.form["job_type"]
        job.description = request.form["description"]
        job.requirements = request.form["requirements"]

        db.session.commit()

        flash("Job updated successfully.", "success")

        return redirect(url_for("admin.manage_jobs"))

    return render_template(
        "admin/edit_job.html",
        job=job
    )


@admin_bp.route("/admin/jobs/delete/<int:id>")
@login_required
def delete_job(id):

    job = Job.query.get_or_404(id)

    db.session.delete(job)

    db.session.commit()

    flash("Job deleted successfully.", "success")

    return redirect(url_for("admin.manage_jobs"))