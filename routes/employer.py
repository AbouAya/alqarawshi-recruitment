from flask import Blueprint, render_template

employer_bp = Blueprint("employer", __name__)


@employer_bp.route("/employers")
def employers():
    return render_template("employers.html")


@employer_bp.route("/employer/register")
def employer_register():
    return render_template("employer_register.html")