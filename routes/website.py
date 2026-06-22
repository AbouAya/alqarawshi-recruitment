from flask import Blueprint, render_template
from models import Job

website_bp = Blueprint("website", __name__)

@website_bp.route("/")
def home():

    latest_jobs = Job.query.order_by(
        Job.created_at.desc()
    ).limit(6).all()

    return render_template(
        "index.html",
        latest_jobs=latest_jobs
    )


@website_bp.route("/about")
def about():
    return render_template("about.html")


@website_bp.route("/services")
def services():
    return render_template("services.html")


@website_bp.route("/contact")
def contact():
    return render_template("contact.html")