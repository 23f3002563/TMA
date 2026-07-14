from flask import Blueprint, render_template, request, redirect, url_for, session
from app import db
from app.models import User, StaffProfile, Trek, Booking

staff_bp = Blueprint("staff", __name__, url_prefix="/staff")


@staff_bp.route("/")
def dashboard():

    staff_id = session.get("user_id")

    total_treks = Trek.query.filter_by(staff_id=staff_id).count()

    assigned_treks = Trek.query.filter_by(staff_id=staff_id).all()

    total_trekkers = 0

    for trek in assigned_treks:
        total_trekkers += Booking.query.filter_by(trek_id=trek.id).count()

    return render_template(
        "staff/dashboard.html",
        total_treks=total_treks,
        total_trekkers=total_trekkers
    )

@staff_bp.route("/treks")
def treks():

    staff_id = session.get("user_id")

    treks = Trek.query.filter_by(staff_id=staff_id).all()

    return render_template(
        "staff/treks.html",
        treks=treks
    )

@staff_bp.route("/participants/<int:trek_id>")
def participants(trek_id):

    bookings = Booking.query.filter_by(
        trek_id=trek_id
    ).all()

    return render_template(
        "staff/participants.html",
        bookings=bookings
    )

@staff_bp.route("/treks/update/<int:trek_id>", methods=["GET", "POST"])
def update_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if request.method == "POST":

        trek.available_slots = request.form["available_slots"]
        trek.status = request.form["status"]

        db.session.commit()

        return redirect(url_for("staff.treks"))

    return render_template(
        "staff/update_trek.html",
        trek=trek
    )

@staff_bp.route("/profile", methods=["GET", "POST"])
def profile():

    profile = StaffProfile.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if request.method == "POST":

        profile.phone = request.form["phone"]
        profile.experience = request.form["experience"]
        profile.specialization = request.form["specialization"]

        db.session.commit()

        return redirect(url_for("staff.dashboard"))

    return render_template(
        "staff/profile.html",
        profile=profile
    )