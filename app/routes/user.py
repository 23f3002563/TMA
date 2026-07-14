from flask import Blueprint, render_template, session, redirect, url_for,request
from app.models import User, Trek, Booking
from app import db

user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/user"
)


@user_bp.route("/")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    total_treks = Trek.query.count()

    total_bookings = Booking.query.filter_by(
        user_id=session["user_id"]
    ).count()

    return render_template(
        "user/dashboard.html",
        total_treks=total_treks,
        total_bookings=total_bookings
    )


@user_bp.route("/treks")
def treks():

    search = request.args.get("search")

    if search:

        treks = Trek.query.filter(
            Trek.trek_name.contains(search) |
            Trek.location.contains(search)
        ).all()

    else:

        treks = Trek.query.all()


    return render_template(
        "user/treks.html",
        treks=treks
    )
    


@user_bp.route("/bookings")
def bookings():

    bookings = Booking.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "user/bookings.html",
        bookings=bookings
    )


@user_bp.route("/profile")
def profile():

    user = User.query.get(session["user_id"])

    return render_template(
        "user/profile.html",
        user=user
    )

@user_bp.route("/book/<int:trek_id>")
def book_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    # Prevent overbooking
    if trek.available_slots <= 0:
        return "No slots available."

    # Prevent duplicate booking
    existing_booking = Booking.query.filter_by(
        user_id=session["user_id"],
        trek_id=trek_id
    ).first()

    if existing_booking:
        return "You have already booked this trek."

    booking = Booking(
        user_id=session["user_id"],
        trek_id=trek_id
    )

    trek.available_slots -= 1

    db.session.add(booking)
    db.session.commit()

    return redirect(url_for("user.bookings")) 

@user_bp.route("/cancel/<int:booking_id>")
def cancel_booking(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != session["user_id"]:
        return "Unauthorized"

    trek = booking.trek
    trek.available_slots += 1

    db.session.delete(booking)
    db.session.commit()

    return redirect(url_for("user.bookings"))