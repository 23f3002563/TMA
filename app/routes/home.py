from flask import Blueprint, render_template

# Create Blueprint
home_bp = Blueprint("home", __name__)

# Home Page
@home_bp.route("/")
def home():
    return render_template("index.html")

# About Page
@home_bp.route("/about")
def about():
    return render_template("about.html")

# Contact Page
@home_bp.route("/contact")
def contact():
    return render_template("contact.html")