from flask import Blueprint, render_template, request, redirect, url_for, session
from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:

            if user.role == "Admin":
                return redirect(url_for("admin.dashboard"))

            elif user.role == "staff":
                return redirect(url_for("staff.dashboard"))

            else:
                return redirect(url_for("user.dashboard"))

    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        new_user = User(
            name=name,
            email=email,
            password=password,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")