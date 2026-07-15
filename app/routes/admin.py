from flask import Blueprint, render_template, request, redirect, url_for
from app.models import User, StaffProfile, Trek, Booking
from app import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
def dashboard():

    total_users = User.query.filter_by(role="user").count()

    total_staff = StaffProfile.query.count()

    total_treks = Trek.query.count()

    total_bookings = Booking.query.count()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_staff=total_staff,
        total_treks=total_treks,
        total_bookings=total_bookings
    )


@admin_bp.route("/users")
def users():

    search = request.args.get("search")

    if search:
        users = User.query.filter(
            User.role == "user",
            User.name.ilike(f"%{search}%")
        ).all()
    else:
        users = User.query.filter_by(role="user").all()

    return render_template(
        "admin/users.html",
        users=users
    )
@admin_bp.route("/staff")
def staff():

    staff_members = StaffProfile.query.all()

    return render_template(
        "admin/staff.html",
        staff_members=staff_members
    )


@admin_bp.route("/treks")
def treks():

    treks = Trek.query.all()

    return render_template(
        "admin/treks.html",
        treks=treks
    )


@admin_bp.route("/bookings")
def bookings():

    bookings = Booking.query.all()

    return render_template(
        "admin/bookings.html",
        bookings=bookings
    )

@admin_bp.route("/treks/add", methods=["GET", "POST"])
def add_trek():

    if request.method == "POST":

        staff_id = request.form["staff_id"]

        trek = Trek(
            trek_name=request.form["trek_name"],
            location=request.form["location"],
            difficulty=request.form["difficulty"],
            duration=request.form["duration"],
            available_slots=request.form["available_slots"],
            staff_id=staff_id
        )

        db.session.add(trek)
        db.session.commit()

        return redirect(url_for("admin.treks"))

    staff_members = User.query.filter_by(role="staff").all()

    return render_template(
        "admin/add_trek.html",
        staff_members=staff_members
    )

@admin_bp.route("/treks/edit/<int:trek_id>", methods=["GET", "POST"])
def edit_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    staff_members = User.query.filter_by(role="staff").all()

    if request.method == "POST":

        trek.trek_name = request.form["trek_name"]
        trek.location = request.form["location"]
        trek.difficulty = request.form["difficulty"]
        trek.duration = request.form["duration"]
        trek.available_slots = request.form["available_slots"]
        trek.staff_id = request.form["staff_id"]

        db.session.commit()

        return redirect(url_for("admin.treks"))

    return render_template(
        "admin/edit_trek.html",
        trek=trek,
        staff_members=staff_members
    )

@admin_bp.route("/treks/delete/<int:trek_id>")
def delete_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    db.session.delete(trek)
    db.session.commit()

    return redirect(url_for("admin.treks"))

@admin_bp.route("/users/deactivate/<int:user_id>")
def deactivate_user(user_id):

    user = User.query.get_or_404(user_id)

    user.is_active = False

    db.session.commit()

    return redirect(url_for("admin.users"))