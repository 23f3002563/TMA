from flask import Blueprint, render_template, session
from app import db
from app.models import Trek, Booking

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


@staff_bp.route("/participants")
def participants():
    return render_template("staff/participants.html")

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