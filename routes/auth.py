from flask import Blueprint, render_template, request, redirect, url_for

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    return redirect(url_for("website.home"))
